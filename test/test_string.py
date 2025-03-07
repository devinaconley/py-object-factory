"""
module for testing functionality of serializable String field
"""

# lib
import pytest
import marshmallow

# src
from objectfactory import Serializable, String


class TestString(object):
    """
    test case for string field type
    """

    def test_definition(self):
        """
        test definition of class with string field

        expect field to be collected, registered, and included
        in schema creation
        """

        class MyTestClass(Serializable):
            str_prop = String()

        assert isinstance(MyTestClass._fields, dict)
        assert len(MyTestClass._fields) == 1
        assert 'str_prop' in MyTestClass._fields
        assert isinstance(MyTestClass._fields['str_prop'], String)

        schema = MyTestClass._schema
        assert issubclass(schema, marshmallow.Schema)
        assert len(schema._declared_fields) == 1
        assert 'str_prop' in schema._declared_fields

        prop = schema._declared_fields['str_prop']
        assert isinstance(prop, marshmallow.fields.String)

    def test_serialize(self):
        """
        test serialize

        expect string data to be dumped to json body
        """

        class MyTestClass(Serializable):
            str_prop = String()

        obj = MyTestClass()
        obj.str_prop = 'some string'

        body = obj.serialize()

        assert body['_type'] == 'test.test_string.MyTestClass'
        assert body['str_prop'] == 'some string'

    def test_deserialize(self):
        """
        test deserialization

        expect string data to be loaded into class
        """

        class MyTestClass(Serializable):
            str_prop = String()

        body = {
            '_type': 'MyTestClass',
            'str_prop': 'another string'
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.str_prop) == str
        assert obj.str_prop == 'another string'

    def test_deserialize_invalid(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid string data
        """

        class MyTestClass(Serializable):
            str_prop = String()

        body = {
            '_type': 'MyTestClass',
            'str_prop': 1000
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.ValidationError):
            obj.deserialize(body)
