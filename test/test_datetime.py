"""
module for testing functionality of serializable datetime field
"""

# lib
import pytest
import marshmallow
import datetime
import zoneinfo

# src
from objectfactory import Serializable, DateTime


class TestDateTime(object):
    """
    test case for datetime field type
    """

    def test_definition(self):
        """
        test definition of class with datetime field

        expect field to be collected, registered, and included
        in schema creation
        """

        class MyTestClass(Serializable):
            datetime_prop = DateTime()

        assert isinstance(MyTestClass._fields, dict)
        assert len(MyTestClass._fields) == 1
        assert 'datetime_prop' in MyTestClass._fields
        assert isinstance(MyTestClass._fields['datetime_prop'], DateTime)

        schema = MyTestClass._schema
        assert issubclass(schema, marshmallow.Schema)
        assert len(schema._declared_fields) == 1
        assert 'datetime_prop' in schema._declared_fields

        prop = schema._declared_fields['datetime_prop']
        assert isinstance(prop, marshmallow.fields.DateTime)

    def test_serialize(self):
        """
        test serialize

        expect datetime data to be dumped to json body
        """

        class MyTestClass(Serializable):
            datetime_prop = DateTime()

        obj = MyTestClass()
        obj.datetime_prop = datetime.datetime(year=2024, month=1, day=14, hour=6, minute=30)

        body = obj.serialize()

        assert body['_type'] == 'test.test_datetime.MyTestClass'
        assert body['datetime_prop'] == '2024-01-14T06:30:00'

    def test_deserialize(self):
        """
        test deserialization

        expect string datetime data to be loaded into field
        """

        class MyTestClass(Serializable):
            datetime_prop = DateTime()

        body = {
            '_type': 'MyTestClass',
            'datetime_prop': '2000-01-01T00:00:00'
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.datetime_prop) == datetime.datetime
        assert obj.datetime_prop == datetime.datetime(year=2000, month=1, day=1)

    def test_serialize_custom(self):
        """
        test serialize

        expect datetime data to be dumped to json body with custom date string format
        """

        class MyTestClass(Serializable):
            datetime_prop = DateTime(date_format='%Y/%m/%d')

        obj = MyTestClass()
        obj.datetime_prop = datetime.datetime(year=2024, month=1, day=14, hour=6, minute=30)

        body = obj.serialize()

        assert body['_type'] == 'test.test_datetime.MyTestClass'
        assert body['datetime_prop'] == '2024/01/14'

    def test_deserialize_custom(self):
        """
        test deserialization casting

        expect datetime data to be loaded from custom date string format
        """

        class MyTestClass(Serializable):
            datetime_prop = DateTime(date_format='%Y/%m/%d')

        body = {
            '_type': 'MyTestClass',
            'datetime_prop': '2010/10/10'
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.datetime_prop) == datetime.datetime
        assert obj.datetime_prop == datetime.datetime(year=2010, month=10, day=10)

    def test_serialize_tz(self):
        """
        test serialize

        expect datetime data to be dumped to json body with timezone
        """

        class MyTestClass(Serializable):
            datetime_prop = DateTime()

        obj = MyTestClass()
        obj.datetime_prop = datetime.datetime(
            year=2024, month=1, day=14, hour=6, minute=30,
            tzinfo=zoneinfo.ZoneInfo('EST')
        )

        body = obj.serialize()

        assert body['_type'] == 'test.test_datetime.MyTestClass'
        assert body['datetime_prop'] == '2024-01-14T06:30:00-05:00'
