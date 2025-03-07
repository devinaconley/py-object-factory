"""
module for testing functionality of serializable enum field
"""

# lib
import pytest
import marshmallow
import enum

# src
from objectfactory import Serializable, Enum


class TestEnum(object):
    """
    test case for enum field type
    """

    def test_definition(self):
        """
        test definition of class with enum field

        expect enum field to be collected, registered, and included
        in schema creation
        """

        class Color(enum.Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        class MyTestClass(Serializable):
            enum_prop = Enum(Color)

        assert isinstance(MyTestClass._fields, dict)
        assert len(MyTestClass._fields) == 1
        assert 'enum_prop' in MyTestClass._fields
        assert isinstance(MyTestClass._fields['enum_prop'], Enum)

        schema = MyTestClass._schema
        assert issubclass(schema, marshmallow.Schema)
        assert len(schema._declared_fields) == 1
        assert 'enum_prop' in schema._declared_fields

        prop = schema._declared_fields['enum_prop']
        assert isinstance(prop, marshmallow.fields.Enum)

    def test_serialize(self):
        """
        test serialize
        expect enum data to be dumped to json body
        """

        class Color(enum.Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        class MyTestClass(Serializable):
            enum_prop = Enum(Color)

        obj = MyTestClass()
        obj.enum_prop = Color.GREEN

        body = obj.serialize()

        assert body['_type'] == 'test.test_enum.MyTestClass'
        assert body['enum_prop'] == 'GREEN'

    def test_deserialize(self):
        """
        test deserialization
        expect string enum data to be loaded into field
        """

        class Color(enum.Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        class MyTestClass(Serializable):
            enum_prop = Enum(Color)

        body = {
            '_type': 'MyTestClass',
            'enum_prop': 'GREEN'
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.enum_prop) == Color
        assert obj.enum_prop == Color.GREEN

    def test_serialize_by_value(self):
        """
        test serialize

        expect enum data to be dumped to json body by name
        """

        class Color(enum.Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        class MyTestClass(Serializable):
            enum_prop = Enum(Color, by_value=True)
            other_enum = Enum(Color, by_value=True)

        obj = MyTestClass()
        obj.enum_prop = Color.BLUE
        obj.other_enum = Color.RED

        body = obj.serialize()

        assert body['_type'] == 'test.test_enum.MyTestClass'
        assert body['enum_prop'] == 3  # 'BLUE'
        assert body['other_enum'] == 1  # 'RED'

    def test_deserialize_by_value(self):
        """
        test deserialization casting
        expect enum data to be loaded properly by name
        """

        class Color(enum.Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        class MyTestClass(Serializable):
            enum_prop = Enum(Color, by_value=True)

        body = {
            '_type': 'MyTestClass',
            'enum_prop': 3
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert type(obj.enum_prop) == Color
        assert obj.enum_prop == Color.BLUE
