"""
module for testing functionality of serializable Float field
"""

# lib
import pytest
import marshmallow

# src
from objectfactory import Serializable, Float


class TestFloat(object):
    """
    test case for float field type
    """

    def test_definition(self):
        """
        test definition of class with float field

        expect field to be collected, registered, and included
        in schema creation
        """

        class MyTestClass(Serializable):
            float_prop = Float()

        assert isinstance(MyTestClass._fields, dict)
        assert len(MyTestClass._fields) == 1
        assert 'float_prop' in MyTestClass._fields
        assert isinstance(MyTestClass._fields['float_prop'], Float)

        schema = MyTestClass._schema
        assert issubclass(schema, marshmallow.Schema)
        assert len(schema._declared_fields) == 1
        assert 'float_prop' in schema._declared_fields

        prop = schema._declared_fields['float_prop']
        assert isinstance(prop, marshmallow.fields.Float)

    def test_serialize(self):
        """
        test serialize

        expect float data to be dumped to json body
        """

        class MyTestClass(Serializable):
            float_prop = Float()

        obj = MyTestClass()
        obj.float_prop = 99.99

        body = obj.serialize()

        assert body['_type'] == 'test.test_float.MyTestClass'
        assert body['float_prop'] == 99.99

    def test_deserialize(self):
        """
        test deserialization

        expect float data to be loaded into class
        """

        class MyTestClass(Serializable):
            float_prop = Float()

        body = {
            '_type': 'MyTestClass',
            'float_prop': 99.99
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.float_prop) == float
        assert obj.float_prop == 99.99

    def test_deserialize_cast(self):
        """
        test deserialization casting

        expect int data to be cast to float
        """

        class MyTestClass(Serializable):
            float_prop = Float()

        body = {
            '_type': 'MyTestClass',
            'float_prop': 99
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.float_prop) == float
        assert obj.float_prop == 99.0

    def test_deserialize_invalid(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid float data
        """

        class MyTestClass(Serializable):
            float_prop = Float()

        body = {
            '_type': 'MyTestClass',
            'float_prop': 'not an float'
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.ValidationError):
            obj.deserialize(body)
