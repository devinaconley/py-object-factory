"""
module for testing custom marshmallow schema
"""

# lib
import datetime
import pytest
import marshmallow

# src
from objectfactory import Serializable, Field


class TestCustomSchema(object):
    """
    test group for custom marshmallow serialization schema
    """

    def test_serialize(self):
        """
        test serialize

        expect date field to be serialized to a string (YYYY-MM-DD)
        """

        class CustomSchema(marshmallow.Schema):
            date = marshmallow.fields.Date()

        class MyTestClass(Serializable, schema=CustomSchema):
            date = Field()

        obj = MyTestClass()
        obj.date = datetime.date(2012, 3, 4)

        body = obj.serialize()

        assert body['_type'] == 'test.test_custom_schema.MyTestClass'
        assert body['date'] == '2012-03-04'

    def test_deserialize(self):
        """
        test deserialize

        expect date field to be loaded from date string encoding (YYYY-MM-DD)
        """

        class CustomSchema(marshmallow.Schema):
            date = marshmallow.fields.Date()

        class MyTestClass(Serializable, schema=CustomSchema):
            date = Field()

        body = {
            '_type': 'MyTestClass',
            'date': '2012-03-04'
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.date.year == 2012
        assert obj.date.month == 3
        assert obj.date.day == 4

    def test_deserialize_invalid(self):
        """
        test deserialize

        expect exception to be thrown on invalid date string
        """

        class CustomSchema(marshmallow.Schema):
            date = marshmallow.fields.Date()

        class MyTestClass(Serializable, schema=CustomSchema):
            date = Field()

        body = {
            '_type': 'MyTestClass',
            'date': '2012-03-45'
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.exceptions.ValidationError):
            obj.deserialize(body)


class TestCustomField(object):
    """
    test group for custom marshmallow field
    """

    def test_serialize(self):
        """
        test serialize

        expect property to be serialized to a lowercase string
        """

        class CustomField(marshmallow.fields.Field):
            def _serialize(self, value, *args, **kwargs):
                return str(value).lower()

        class CustomSchema(marshmallow.Schema):
            str_prop = CustomField()

        class MyTestClass(Serializable, schema=CustomSchema):
            str_prop = Field()

        obj = MyTestClass()
        obj.str_prop = 'HELLO'

        body = obj.serialize()

        assert body['_type'] == 'test.test_custom_schema.MyTestClass'
        assert body['str_prop'] == 'hello'

    def test_deserialize(self):
        """
        test deserialize

        expect string to be loaded and formatted as all uppercase
        """

        class CustomField(marshmallow.fields.Field):
            def _deserialize(self, value, *args, **kwargs):
                if len(value) > 8:
                    raise marshmallow.ValidationError('Field too long')
                return str(value).upper()

        class CustomSchema(marshmallow.Schema):
            str_prop = CustomField()

        class MyTestClass(Serializable, schema=CustomSchema):
            str_prop = Field()

        body = {
            '_type': 'MyTestClass',
            'str_prop': 'hello'
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.str_prop == 'HELLO'

    def test_deserialize_invalid(self):
        """
        test deserialize

        expect exception to be thrown on too long of a string
        """

        class CustomField(marshmallow.fields.Field):
            def _deserialize(self, value, *args, **kwargs):
                if len(value) > 8:
                    raise marshmallow.ValidationError('Field too long')
                return str(value).upper()

        class CustomSchema(marshmallow.Schema):
            str_prop = CustomField()

        class MyTestClass(Serializable, schema=CustomSchema):
            str_prop = Field()

        body = {
            '_type': 'MyTestClass',
            'str_prop': 'helloworld'
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.exceptions.ValidationError):
            obj.deserialize(body)
