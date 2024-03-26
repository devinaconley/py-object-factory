"""
module for testing functionality of serializable Integer field
"""

# lib
import pytest
import marshmallow

# src
from objectfactory import Serializable, Integer


class TestInteger(object):
    """
    test case for integer field type
    """

    def test_definition(self):
        """
        test definition of class with integer field

        expect field to be collected, registered, and included
        in schema creation
        """

        class MyTestClass(Serializable):
            int_prop = Integer()

        assert isinstance(MyTestClass._fields, dict)
        assert len(MyTestClass._fields) == 1
        assert 'int_prop' in MyTestClass._fields
        assert isinstance(MyTestClass._fields['int_prop'], Integer)

        schema = MyTestClass._schema
        assert issubclass(schema, marshmallow.Schema)
        assert len(schema._declared_fields) == 1
        assert 'int_prop' in schema._declared_fields

        prop = schema._declared_fields['int_prop']
        assert isinstance(prop, marshmallow.fields.Integer)

    def test_serialize(self):
        """
        test serialize

        expect integer data to be dumped to json body
        """

        class MyTestClass(Serializable):
            int_prop = Integer()

        obj = MyTestClass()
        obj.int_prop = 99

        body = obj.serialize()

        assert body['_type'] == 'test.test_integer.MyTestClass'
        assert body['int_prop'] == 99

    def test_deserialize(self):
        """
        test deserialization

        expect integer data to be loaded into class
        """

        class MyTestClass(Serializable):
            int_prop = Integer()

        body = {
            '_type': 'MyTestClass',
            'int_prop': 99
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.int_prop == 99

    def test_deserialize_cast(self):
        """
        test deserialization casting

        expect float data to be cast to integer
        """

        class MyTestClass(Serializable):
            int_prop = Integer()

        body = {
            '_type': 'MyTestClass',
            'int_prop': 99.01
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.int_prop) == int
        assert obj.int_prop == 99

    def test_deserialize_invalid(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid integer data
        """

        class MyTestClass(Serializable):
            int_prop = Integer()

        body = {
            '_type': 'MyTestClass',
            'int_prop': 'not an integer'
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.ValidationError):
            obj.deserialize(body)
