"""
module for testing functionality of serializable Boolean field
"""

# lib
import pytest
import marshmallow

# src
from objectfactory import Serializable, Boolean


class TestBoolean(object):
    """
    test case for boolean field type
    """

    def test_definition(self):
        """
        test definition of class with boolean field

        expect field to be collected, registered, and included
        in schema creation
        """

        class MyTestClass(Serializable):
            bool_prop = Boolean()

        assert isinstance(MyTestClass._fields, dict)
        assert len(MyTestClass._fields) == 1
        assert 'bool_prop' in MyTestClass._fields
        assert isinstance(MyTestClass._fields['bool_prop'], Boolean)

        schema = MyTestClass._schema
        assert issubclass(schema, marshmallow.Schema)
        assert len(schema._declared_fields) == 1
        assert 'bool_prop' in schema._declared_fields

        prop = schema._declared_fields['bool_prop']
        assert isinstance(prop, marshmallow.fields.Boolean)

    def test_serialize(self):
        """
        test serialize

        expect boolean data to be dumped to json body
        """

        class MyTestClass(Serializable):
            bool_prop = Boolean()

        obj = MyTestClass()
        obj.bool_prop = True

        body = obj.serialize()

        assert body['_type'] == 'test.test_boolean.MyTestClass'
        assert body['bool_prop'] == True

    def test_deserialize(self):
        """
        test deserialization

        expect boolean data to be loaded into class
        """

        class MyTestClass(Serializable):
            bool_prop = Boolean()

        body = {
            '_type': 'MyTestClass',
            'bool_prop': True
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.bool_prop) == bool
        assert obj.bool_prop == True

    def test_deserialize_cast(self):
        """
        test deserialization casting

        expect int data to be cast to boolean
        """

        class MyTestClass(Serializable):
            bool_prop = Boolean()

        body = {
            '_type': 'MyTestClass',
            'bool_prop': 1
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.bool_prop) == bool
        assert obj.bool_prop == True

        body = {
            '_type': 'MyTestClass',
            'bool_prop': 0
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.bool_prop) == bool
        assert obj.bool_prop == False

    def test_deserialize_invalid_int(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid boolean data from
        int not in [0, 1]
        """

        class MyTestClass(Serializable):
            bool_prop = Boolean()

        body = {
            '_type': 'MyTestClass',
            'bool_prop': 2
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.ValidationError):
            obj.deserialize(body)

    def test_deserialize_invalid_float(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid boolean data from float
        """

        class MyTestClass(Serializable):
            bool_prop = Boolean()

        body = {
            '_type': 'MyTestClass',
            'bool_prop': 1.1
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.ValidationError):
            obj.deserialize(body)

    def test_deserialize_invalid_string(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid boolean data from string
        """

        class MyTestClass(Serializable):
            bool_prop = Boolean()

        body = {
            '_type': 'MyTestClass',
            'bool_prop': 'helloworld'
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.ValidationError):
            obj.deserialize(body)
