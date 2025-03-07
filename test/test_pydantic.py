"""
module for testing functionality of serializable objects
"""

# lib

# src
from test.testmodule.testclasses import MyTestClass, MyTestSubclass


class TestSerializableObject(object):
    """
    test group for normal python usage of serializable object
    """

    def test_init_keywords(self):
        """
        test initializing class with keywords based on fields

        expect any fields to pass through as a keyword arg to init
        """
        obj = MyTestClass.from_kwargs(
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
        obj = MyTestClass.from_dict(
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
        obj = MyTestClass(
            str_prop='my awesome string',
            int_prop=1234
        )
        body = obj.serialize()

        assert body['_type'] == 'test.testmodule.testclasses.MyTestClass'
        assert body['str_prop'] == 'my awesome string'
        assert body['int_prop'] == 1234

    def test_deserialize(self):
        """
        test deserialization
        """
        body = {
            '_type': 'MyTestClass',
            'str_prop': 'another great string',
            'int_prop': 9001
        }

        obj = MyTestClass.from_dict(body)

        assert isinstance(obj, MyTestClass)
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
        obj1 = MyTestClass.from_dict(body1)
        obj2 = MyTestClass.from_dict(body2)

        assert isinstance(obj1, MyTestClass)
        assert obj1.str_prop == 'string1'
        assert obj1.int_prop == 9001

        assert isinstance(obj2, MyTestClass)
        assert obj2.str_prop == 'string2'
        assert obj2.int_prop == 9002

    def test_serialize_short_type(self):
        """
        test serialization without fully qualified path

        expect short name to be set as value in type field
        """
        obj = MyTestClass(
            str_prop='my awesome string',
            int_prop=1234
        )
        body = obj.serialize(use_full_type=False)

        assert body['_type'] == 'MyTestClass'
        assert body['str_prop'] == 'my awesome string'
        assert body['int_prop'] == 1234

    def test_serialize_no_type(self):
        """
        test serialization without type info

        expect _type key to be excluded
        """
        obj = MyTestClass(
            str_prop='my awesome string',
            int_prop=1234
        )
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

        expect members of both parent and subclass to be serialized, _type string
        should be MySubClass, and override should not cause conflict
        """
        obj = MyTestSubclass(
            str_prop='parent_class_string',
            int_prop=99,
            str_prop_sub='sub_class_string'
        )

        body = obj.serialize()

        assert body['_type'] == 'test.testmodule.testclasses.MyTestSubclass'
        assert body['str_prop'] == 'parent_class_string'
        assert body['int_prop'] == 99
        assert body['str_prop_sub'] == 'sub_class_string'

    def test_deserialize(self):
        """
        test deserialization

        expect both parent and subclass members to be properly loaded, obj type
        should be MySubClass, and override should not cause conflict
        """
        body = {
            '_type': 'MySubClass',
            'str_prop': 'parent_class_string',
            'int_prop': 99,
            'str_prop_sub': 'sub_class_string'
        }

        obj = MyTestSubclass.from_dict(body)

        assert isinstance(obj, MyTestSubclass)
        assert obj.str_prop == 'parent_class_string'
        assert obj.int_prop == 99
        assert obj.str_prop_sub == 'sub_class_string'
