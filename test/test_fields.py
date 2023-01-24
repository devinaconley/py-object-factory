"""
module for testing serializable List field
"""

# lib
import pytest
import marshmallow

# src
from objectfactory import Serializable, Field


class TestFieldOptionals(object):
    """
    test case for optional params to field arguments
    """

    def test_serialize_default(self):
        """
        test serialization

        expect default value to be serialized for unset str_prop
        """

        class MyTestClass(Serializable):
            str_prop = Field(default='default_val')

        obj = MyTestClass()

        assert obj.str_prop == 'default_val'

        body = obj.serialize()

        assert body['_type'] == 'test.test_fields.MyTestClass'
        assert body['str_prop'] == 'default_val'

    def test_deserialize_default(self):
        """
        test deserialization

        expect default value to be loaded into str_prop if not specified, and
        int_prop_named to be deserialized into int_prop
        """

        class MyTestClass(Serializable):
            str_prop = Field(default='default_val')

        body = {
            '_type': 'MyTestClass'
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.str_prop == 'default_val'

    def test_serialize_keyed(self):
        """
        test serialization

        expect int_prop to be serialized under key int_prop_named
        """

        class MyTestClass(Serializable):
            int_prop = Field(key='int_prop_named')

        obj = MyTestClass()
        obj.int_prop = 99

        body = obj.serialize()

        assert body['_type'] == 'test.test_fields.MyTestClass'
        assert body['int_prop_named'] == 99

    def test_deserialize_keyed(self):
        """
        test deserialization

        expect int_prop_named to be deserialized into int_prop
        """

        class MyTestClass(Serializable):
            int_prop = Field(key='int_prop_named')

        body = {
            '_type': 'MyTestClass',
            'int_prop_named': 99
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.int_prop == 99

    def test_deserialize_required(self):
        """
        test deserialization of required field

        expect required property to be deserialized into prop
        """

        class MyTestClass(Serializable):
            prop = Field(required=True)

        body = {
            '_type': 'MyTestClass',
            'prop': 42
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.prop == 42

    def test_deserialize_required_missing(self):
        """
        test deserialization of required field

        expect exception to be thrown on missing prop field
        """

        class MyTestClass(Serializable):
            prop = Field(required=True)

        body = {
            '_type': 'MyTestClass'
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.exceptions.ValidationError):
            obj.deserialize(body)

    def test_deserialize_null(self):
        """
        test deserialization validation

        expect null to be deserialized to None
        """

        class MyTestClass(Serializable):
            prop = Field()

        body = {
            '_type': 'MyTestClass',
            'prop': None
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.prop is None

    def test_deserialize_null_disallowed(self):
        """
        test deserialization validation

        expect exception to be thrown when null value is not allowed
        """

        class MyTestClass(Serializable):
            prop = Field(allow_none=False)

        body = {
            '_type': 'MyTestClass',
            'prop': None
        }

        obj = MyTestClass()
        with pytest.raises(marshmallow.exceptions.ValidationError):
            obj.deserialize(body)
