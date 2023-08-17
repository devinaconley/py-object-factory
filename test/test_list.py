"""
module for testing functionality of serializable list field
"""

# lib
import pytest
import marshmallow

# src
import objectfactory
from objectfactory import Serializable, List, String, Integer, register


class TestPrimitiveList(object):
    """
    test case for serialization of basic lists of primitive strings and integers
    """

    def test_serialize(self):
        """
        test serialization

        expect list within a standard field to function as standard list object
        and to dump up-to-date list of all primitive values
        """

        class MyTestClass(Serializable):
            str_list_prop = List(field_type=String)
            int_list_prop = List(field_type=Integer)

        obj = MyTestClass()
        obj.str_list_prop = ['hello', 'world']
        obj.int_list_prop = [0, 1, 2, 3, 4]
        obj.str_list_prop.append('!')
        obj.int_list_prop.append(5)
        body = obj.serialize()

        assert body['_type'] == 'test.test_list.MyTestClass'
        assert body['str_list_prop'] == ['hello', 'world', '!']
        assert body['int_list_prop'] == [0, 1, 2, 3, 4, 5]

    def test_deserialize(self):
        """
        test deserialization

        expect json list of primitives to be loaded properly into
        serializable object
        """

        class MyTestClass(Serializable):
            str_list_prop = List(field_type=String)
            int_list_prop = List(field_type=Integer)

        body = {
            '_type': 'MyTestClass',
            'str_list_prop': ['my', 'awesome', 'list', 'of', 'strings'],
            'int_list_prop': [9001, 9002, 9003]
        }

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.str_list_prop == ['my', 'awesome', 'list', 'of', 'strings']
        assert obj.int_list_prop == [9001, 9002, 9003]

    def test_deserialize_invalid(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid integer data
        """

        class MyTestClass(Serializable):
            str_list_prop = List(field_type=String)
            int_list_prop = List(field_type=Integer)

        body = {
            '_type': 'MyTestClass',
            'str_list_prop': ['my', 'awesome', 'list', 'of', 'strings'],
            'int_list_prop': [9001, 9002, 9003, 'string']
        }

        obj = MyTestClass()

        with pytest.raises(marshmallow.ValidationError):
            obj.deserialize(body)

    def test_serialize_deep_copy(self):
        """
        test serialization

        expect modification to original list to have no effect on
        serialized json body
        """

        class MyTestClass(Serializable):
            str_list_prop = List(field_type=String)
            int_list_prop = List(field_type=Integer)

        obj = MyTestClass()
        obj.str_list_prop = ['hello', 'world']
        obj.int_list_prop = [0, 1, 2, 3, 4]
        body = obj.serialize()

        obj.str_list_prop.append('!')
        obj.int_list_prop.append(5)

        assert body['_type'] == 'test.test_list.MyTestClass'
        assert body['str_list_prop'] == ['hello', 'world']
        assert body['int_list_prop'] == [0, 1, 2, 3, 4]

    def test_deserialize_deep_copy(self):
        """
        test deserialization

        expect modification to original json list of primitives to
        have not effect on loaded serializable object
        """

        class MyTestClass(Serializable):
            str_list_prop = List(field_type=String)
            int_list_prop = List(field_type=Integer)

        body = {
            '_type': 'MyTestClass',
            'str_list_prop': ['my', 'awesome', 'list', 'of', 'strings'],
            'int_list_prop': [9001, 9002, 9003]
        }

        obj = MyTestClass()
        obj.deserialize(body)

        body['str_list_prop'].pop()
        body['int_list_prop'].pop()

        assert isinstance(obj, MyTestClass)
        assert obj.str_list_prop == ['my', 'awesome', 'list', 'of', 'strings']
        assert obj.int_list_prop == [9001, 9002, 9003]


class TestNestedList(object):
    """
    test case for model containing a list of nested serializable objects
    """

    def setup_method(self, _):
        """
        prepare for each test
        """
        objectfactory.factory._global_factory.registry.clear()

    def test_serializable(self):
        """
        test serialization

        expect all nested instances of MyNestedClass to populate a list
        in json body of MyTestClass
        """

        @register
        class MyNestedClass(Serializable):
            str_prop = String()
            int_prop = Integer()

        class MyTestClass(Serializable):
            str_prop = String()
            nested_list_prop = List()

        obj = MyTestClass()
        obj.str_prop = 'object name'
        obj.nested_list_prop = []

        nested_strings = ['some string', 'another string', 'one more string']
        nested_ints = [101, 102, 103]

        for s, n in zip(nested_strings, nested_ints):
            temp = MyNestedClass()
            temp.str_prop = s
            temp.int_prop = n
            obj.nested_list_prop.append(temp)

        body = obj.serialize()

        assert body['_type'] == 'test.test_list.MyTestClass'
        assert body['str_prop'] == 'object name'
        assert len(body['nested_list_prop']) == 3
        for i, nested_body in enumerate(body['nested_list_prop']):
            assert nested_body['_type'] == 'test.test_list.MyNestedClass'
            assert nested_body['str_prop'] == nested_strings[i]
            assert nested_body['int_prop'] == nested_ints[i]

    def test_deserialize(self):
        """
        test deserialization

        expect list of nested json objects to be deserialized into a list
        of MyNestedClass objects that is a member of MyTestClass
        """

        @register
        class MyNestedClass(Serializable):
            str_prop = String()
            int_prop = Integer()

        class MyTestClass(Serializable):
            str_prop = String()
            nested_list_prop = List()

        body = {
            '_type': 'MyTestClass',
            'str_prop': 'really great string property',
            'nested_list_prop': []
        }
        nested_strings = ['some string', 'another string', 'one more string']
        nested_ints = [101, 102, 103]

        for s, n in zip(nested_strings, nested_ints):
            body['nested_list_prop'].append(
                {
                    '_type': 'MyNestedClass',
                    'str_prop': s,
                    'int_prop': n
                }
            )

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.str_prop == 'really great string property'
        assert len(obj.nested_list_prop) == 3
        for i, nested_obj in enumerate(obj.nested_list_prop):
            assert isinstance(nested_obj, MyNestedClass)
            assert nested_obj.str_prop == nested_strings[i]
            assert nested_obj.int_prop == nested_ints[i]

    def test_deserialize_typed(self):
        """
        test deserialization without _type field

        expect list of nested json objects to be deserialized into a list
        of MyNestedClass objects that is a member of MyTestClass, even without
        _type field specified
        """

        @register
        class MyNestedClass(Serializable):
            str_prop = String()
            int_prop = Integer()

        class MyTestClass(Serializable):
            str_prop = String()
            nested_list_prop = List(field_type=MyNestedClass)

        body = {
            '_type': 'MyTestClass',
            'str_prop': 'really great string property',
            'nested_list_prop': []
        }
        nested_strings = ['some string', 'another string', 'one more string']
        nested_ints = [101, 102, 103]

        for s, n in zip(nested_strings, nested_ints):
            body['nested_list_prop'].append(
                {
                    'str_prop': s,
                    'int_prop': n
                }
            )

        obj = MyTestClass()
        obj.deserialize(body)

        assert isinstance(obj, MyTestClass)
        assert obj.str_prop == 'really great string property'
        assert len(obj.nested_list_prop) == 3
        for i, nested_obj in enumerate(obj.nested_list_prop):
            assert isinstance(nested_obj, MyNestedClass)
            assert nested_obj.str_prop == nested_strings[i]
            assert nested_obj.int_prop == nested_ints[i]

    def test_deserialize_typed_invalid(self):
        """
        test deserialization validation

        expect validation error to be raised on invalid nested object type
        """

        @register
        class MyNestedClass(Serializable):
            str_prop = String()

        @register
        class OtherClass(Serializable):
            str_prop = String()

        class MyTestClass(Serializable):
            str_prop = String()
            nested_list_prop = List(field_type=MyNestedClass)

        body = {
            '_type': 'MyTestClass',
            'nested_list_prop': [
                {
                    '_type': 'OtherClass',
                    'str_prop': 'some string',
                }
            ]
        }

        obj = MyTestClass()

        with pytest.raises(ValueError):
            obj.deserialize(body)

    def test_default_unique(self):
        """
        test default nested list field is unique between instances

        expect the default value to be replicated for each instance
        of the parent class, to avoid unintentional memory sharing
        """

        @register
        class MyNestedClass(Serializable):
            str_prop = String()
            int_prop = Integer()

        class MyTestClass(Serializable):
            str_prop = Integer()
            nested_list_prop = List()

        obj_a = MyTestClass()
        obj_b = MyTestClass()

        assert len(obj_a.nested_list_prop) == 0
        assert len(obj_b.nested_list_prop) == 0

        obj_a.nested_list_prop.append(MyNestedClass.from_kwargs(str_prop='x'))

        assert len(obj_a.nested_list_prop) == 1
        assert obj_a.nested_list_prop[0].str_prop == 'x'
        assert len(obj_b.nested_list_prop) == 0

        obj_a.nested_list_prop.append(MyNestedClass.from_kwargs(str_prop='y'))
        obj_b.nested_list_prop.append(MyNestedClass.from_kwargs(str_prop='z'))

        assert len(obj_a.nested_list_prop) == 2
        assert obj_a.nested_list_prop[0].str_prop == 'x'
        assert obj_a.nested_list_prop[1].str_prop == 'y'
        assert len(obj_b.nested_list_prop) == 1
        assert obj_b.nested_list_prop[0].str_prop == 'z'
