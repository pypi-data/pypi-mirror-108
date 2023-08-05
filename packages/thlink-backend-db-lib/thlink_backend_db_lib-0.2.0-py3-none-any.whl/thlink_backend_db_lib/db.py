from __future__ import annotations
from typing import Dict, Tuple, Optional, Any
import boto3
import botocore.exceptions
import boto3.dynamodb.conditions


class ItemKey:

    def __init__(self, name, value, secondary: ItemKey = None):
        if secondary and secondary.secondary:
            raise ValueError("ItemKey can only consist of one primary and one secondary key")
        self.name = name
        self.value = value
        self.secondary = secondary

    def as_dynamodb_primary_key_cond_expression(self):
        return boto3.dynamodb.conditions.Key(self.name).eq(self.value)

    def as_dynamodb_key(self):
        return {*{self.name: self.value}, *(self.secondary.as_dynamodb_key() if self.secondary else {})}


class DB:

    def __init__(self, name: str):
        self._table = boto3.resource("dynamodb").Table(name)

    def query_items(self, key: ItemKey):
        # query primary key
        try:
            response = self._table.query(
                IndexName=key.name,
                KeyConditionExpression=key.as_dynamodb_primary_key_cond_expression(),
            )
            return response["Items"]
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e

    def get_item(self, key: ItemKey):
        try:
            resp = self._table.get_item(Key=key.as_dynamodb_key())
            return resp["Item"]
        except botocore.exceptions.ClientError as e:
            raise

    def put(self, key: ItemKey, item: Dict, expect_if_item_exists: Dict = None):
        assert key.name in item
        assert not key.secondary or key.secondary.name in item
        expression_values = {}
        statements = []
        for name, value in expect_if_item_exists.items():
            statements.append(f"{name}=:{name}")
            expression_values[f":{name}"] = value
        condition_expression = " AND ".join(statements)
        if expect_if_item_exists:
            condition_expression = f"({condition_expression}) OR {key.name}<>:{key.name}"
            expression_values[key.name] = key.value
        try:
            self._table.put_item(Item=item, ConditionExpression=condition_expression)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise ExpectationNotMet() from e
            raise InternalError() from e

    def update(self, key: ItemKey, item: Dict, old_item: Dict):
        assert key.name in item
        assert not key.secondary or key.secondary.name in item

        def build_expression():  # apply diff
            statements = []
            values = {}

            for name, attribute in item.items():

                if type(attribute) is dict and name in old_item:
                    for sub_name, sub_attribute in attribute.items():
                        if sub_name not in old_item[name] or old_item[name][sub_name] != sub_attribute:
                            statements.append(f"SET {name}.{sub_name}=:{name}.{sub_name}")
                            values[f":{name}.{sub_name}"] = sub_attribute
                    for old_sub_name in old_item[name]:
                        if old_sub_name not in attribute:
                            statements.append(f"DELETE {name}.{old_sub_name}")

                else:
                    statements.append(f"SET {name}=:{name}")
                    values["name"] = attribute

            for old_name in old_item:
                if old_name not in item:
                    statements.append(f"DELETE {old_name}")

            return ", ".join(statements), values

        expression, expression_values = build_expression()

        try:
            self._table.update_item(
                Key=key.as_dynamodb_key(),
                UpdateExpression=expression,
                ExpressionAttributeValues=expression_values,
                # make sure that item is being updated, not created
                ConditionExpression=f"attribute_exists({key.name})",
            )
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e

    def delete(self, key: ItemKey):
        try:
            self._table.delete_item(Key=key.as_dynamodb_key())
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e


class DBMock:
    _table: Dict[Tuple[str, Optional[str]], Any]

    count_query_operations: int

    def query_items(self, key: ItemKey):
        DBMock.count_query_operations += 1
        items = []
        for found_key, found_item in DBMock._table.items():
            if found_key[0] == key.value:
                items.append(found_item)
        return items

    count_get_operations: int

    def get_item(self, key: ItemKey, count=True):
        if count:
            DBMock.count_get_operations += 1
        return DBMock._table.get(self._key_for_table(key))

    count_put_operations: int

    def put(self, key: ItemKey, item: Dict, expect_if_item_exists: Dict = None, count=True):
        if expect_if_item_exists is None:
            expect_if_item_exists = {}
        if count:
            DBMock.count_put_operations += 1
        assert key.name in item
        assert not key.secondary or key.secondary.name in item
        existing = self.get_item(key, count=False)
        if existing:
            for name, value in expect_if_item_exists.items():
                if existing.get(name) != value:
                    raise ExpectationNotMet()
        DBMock._table[self._key_for_table(key)] = item

    count_update_operations: int

    def update(self, key: ItemKey, item: Dict, old_item: Dict):
        DBMock.count_update_operations += 1
        self.put(key, item, count=False)

    count_delete_operations: int

    def delete(self, key: ItemKey):
        DBMock.count_delete_operations += 1
        if self._key_for_table(key) in self._table:
            del DBMock._table[self._key_for_table(key)]

    @staticmethod
    def test_operations_count(query=0, get=0, put=0, update=0, delete=0):
        assert DBMock.count_query_operations == query
        assert DBMock.count_get_operations == get
        assert DBMock.count_put_operations == put
        assert DBMock.count_update_operations == update
        assert DBMock.count_delete_operations == delete

    @staticmethod
    def _key_for_table(key: ItemKey):
        if key.secondary:
            return key.value, key.secondary.value
        return key.value, None


class ExpectationNotMet(ValueError):
    pass


class InternalError(Exception):
    pass
