"""
module for testing functionality of serializable objects
"""

# lib
import marshmallow

# src
from objectfactory import Serializable, Field
from .testmodule.testclasses import MyBasicClass, MySubClass


class TestClassDefinition(object):
    """
    test group for definition of serializable object
    """

    def test_fields_collected(self):
        """
        test collection of field descriptors

        expect each field defined in serializable class to be detected
        and indexed under the _fields parameter
        """

        class MyClass(Serializable):
            some_field = Field()
            another_field = Field()
            not_a_field = 'some class attribute'

        assert isinstance(MyClass._fields, dict)
        assert len(MyClass._fields) == 2
        assert 'some_field' in MyClass._fields
        assert isinstance(MyClass._fields['some_field'], Field)
        assert 'another_field' in MyClass._fields
        assert isinstance(MyClass._fields['another_field'], Field)
        assert 'not_a_field' not in MyClass._fields

    def test_schema_creation(self):
        """
        test creation of marshmallow schema

        expect schema to contain each field defined in serializable class
        """

        class MyClass(Serializable):
            some_field = Field()
            another_field = Field()

        schema = MyClass._schema
        assert issubclass(schema, marshmallow.Schema)
        assert len(schema._declared_fields) == 2
        assert 'some_field' in schema._declared_fields
        assert isinstance(schema._declared_fields['some_field'], marshmallow.fields.Field)
        assert 'another_field' in schema._declared_fields
        assert isinstance(schema._declared_fields['another_field'], marshmallow.fields.Field)


class TestSerializableObject(object):
    """
    test group for normal python usage of serializable object
    """

    def test_init_keywords(self):
        """
        test initializing class with keywords based on fields

        expect any fields to pass through as a keyword arg to init
        """
        obj = MyBasicClass.from_kwargs(
            str_prop='some string',
            int_prop=12
        )

        assert obj.str_prop == 'some string'
        assert obj.int_prop == 12

    def test_init_dictionary(self):
        """
        test initializing class with dictionary

        expect any dictionary data fields to pass through to init
        """
        obj = MyBasicClass.from_dict(
            {
                'str_prop': 'some string',
                'int_prop': 12
            }
        )

        assert obj.str_prop == 'some string'
        assert obj.int_prop == 12


class TestSerialization(object):
    """
    test group for serialization of basic object with primitive fields
    """

    def test_serialize(self):
        """
        test serialization
        """
        obj = MyBasicClass()
        obj.str_prop = 'my awesome string'
        obj.int_prop = 1234
        body = obj.serialize()

        assert body['_type'] == 'test.testmodule.testclasses.MyBasicClass'
        assert body['str_prop'] == 'my awesome string'
        assert body['int_prop'] == 1234

    def test_deserialize(self):
        """
        test deserialization
        """
        body = {
            '_type': 'MyBasicClass',
            'str_prop': 'another great string',
            'int_prop': 9001
        }

        obj = MyBasicClass()
        obj.deserialize(body)

        assert isinstance(obj, MyBasicClass)
        assert obj.str_prop == 'another great string'
        assert obj.int_prop == 9001

    def test_multiple(self):
        """
        test deserializing multiple objects of same class

        validate there is no conflict in values of class level descriptors
        """
        body1 = {
            '_type': 'MyBasicClass',
            'str_prop': 'string1',
            'int_prop': 9001
        }
        body2 = {
            '_type': 'MyBasicClass',
            'str_prop': 'string2',
            'int_prop': 9002
        }
        obj1 = MyBasicClass()
        obj1.deserialize(body1)
        obj2 = MyBasicClass()
        obj2.deserialize(body2)

        assert isinstance(obj1, MyBasicClass)
        assert obj1.str_prop == 'string1'
        assert obj1.int_prop == 9001

        assert isinstance(obj2, MyBasicClass)
        assert obj2.str_prop == 'string2'
        assert obj2.int_prop == 9002

    def test_serialize_short_type(self):
        """
        test serialization without fully qualified path

        expect short name to be set as value in type field
        """
        obj = MyBasicClass()
        obj.str_prop = 'my awesome string'
        obj.int_prop = 1234
        body = obj.serialize(use_full_type=False)

        assert body['_type'] == 'MyBasicClass'
        assert body['str_prop'] == 'my awesome string'
        assert body['int_prop'] == 1234

    def test_serialize_no_type(self):
        """
        test serialization without type info

        expect _type key to be excluded
        """
        obj = MyBasicClass()
        obj.str_prop = 'my awesome string'
        obj.int_prop = 1234
        body = obj.serialize(include_type=False)

        assert '_type' not in body
        assert body['str_prop'] == 'my awesome string'
        assert body['int_prop'] == 1234


class TestSubClass(object):
    """
    test group for sub-classing another serializable model
    """

    def test_serialize(self):
        """
        test serialization

        expect members of both parent and sub-class to be serialized, _type string
        should be MySubClass, and override should not cause conflict
        """
        obj = MySubClass()
        obj.str_prop = 'parent_class_string'
        obj.int_prop = 99
        obj.str_prop_sub = 'sub_class_string'

        body = obj.serialize()

        assert body['_type'] == 'test.testmodule.testclasses.MySubClass'
        assert body['str_prop'] == 'parent_class_string'
        assert body['int_prop'] == 99
        assert body['str_prop_sub'] == 'sub_class_string'

    def test_deserialize(self):
        """
        test deserialization

        expect both parent and sub-class members to be properly loaded, obj type
        should be MySubClass, and override should not cause conflict
        """
        body = {
            '_type': 'MySubClass',
            'str_prop': 'parent_class_string',
            'int_prop': 99,
            'str_prop_sub': 'sub_class_string'
        }

        obj = MySubClass()
        obj.deserialize(body)

        assert isinstance(obj, MySubClass)
        assert obj.str_prop == 'parent_class_string'
        assert obj.int_prop == 99
        assert obj.str_prop_sub == 'sub_class_string'
