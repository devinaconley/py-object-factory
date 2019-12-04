"""
module for testing functionality of serializable fields
"""

# lib
import pytest

# src
from objectfactory import Factory, Serializable, Field, Nested, List
from .test_serializable import MyBasicClass


@Factory.register_class
class MyBasicClassWithLists( Serializable ):
    """
    basic class to be used for testing serialization of primitive lists
    """
    str_list_prop = Field()
    int_list_prop = Field()


@Factory.register_class
class MyComplexClass( Serializable ):
    """
    complex class to test hierarchical serialization
    """
    nested = Nested()
    prop = Field()


@Factory.register_class
class MyTypedComplexClass( Serializable ):
    """
    complex class to test hierarchical serialization
    """
    nested = Nested( field_type=MyBasicClass )
    prop = Field()


@Factory.register_class
class MyOtherComplexClass( Serializable ):
    """
    complex class to test list serialization
    """
    str_prop = Field()
    nested_list_prop = List()


@Factory.register_class
class MyOtherTypedComplexClass( Serializable ):
    """
    complex class to test list serialization
    """
    str_prop = Field()
    nested_list_prop = List( field_type=MyBasicClass )


@Factory.register_class
class MyClassWithFieldOptionals( Serializable ):
    """
    complex class to test list serialization
    """
    str_prop = Field( default='default_val' )
    int_prop = Field( name='int_prop_named' )


class TestNested( object ):
    """
    test case for hierarchical serializable object with primitive and nested fields
    """

    def test_serialize( self ):
        """
        test serialization

        expect serialized MyBasicClass object to be nested in json body of MyComplexClass

        :return:
        """
        obj = MyComplexClass()
        obj.prop = 'some property'
        obj.nested = MyBasicClass()
        obj.nested.str_prop = 'my subclass string'
        obj.nested.int_prop = 100

        body = obj.serialize()

        assert body['_type'] == 'MyComplexClass'
        assert body['prop'] == 'some property'
        assert body['nested']['_type'] == 'MyBasicClass'
        assert body['nested']['str_prop'] == 'my subclass string'
        assert body['nested']['int_prop'] == 100

    def test_deserialize( self ):
        """
        test deserialization

        expect nested json to be deserialized into a MyBasicClass object that is
        a member of MyComplexClass

        :return:
        """
        body = {
            '_type': 'MyComplexClass',
            'prop': 'really cool property',
            'nested': {
                '_type': 'MyBasicClass',
                'str_prop': 'random string',
                'int_prop': 4321
            }
        }

        obj = MyComplexClass()
        obj.deserialize( body )

        assert isinstance( obj, MyComplexClass )
        assert obj.prop == 'really cool property'
        assert isinstance( obj.nested, MyBasicClass )
        assert obj.nested.str_prop == 'random string'
        assert obj.nested.int_prop == 4321

    def test_deserialize_typed( self ):
        """
        test deserialization without _type field

        expect nested json to be deserialized into a MyBasicClass object that is
        a member of MyTypedComplexClass, even without nested _type field

        :return:
        """
        body = {
            '_type': 'MyComplexClass',
            'prop': 'really cool property',
            'nested': {
                'str_prop': 'random string',
                'int_prop': 4321
            }
        }

        obj = MyTypedComplexClass()
        obj.deserialize( body )

        assert isinstance( obj, MyTypedComplexClass )
        assert obj.prop == 'really cool property'
        assert isinstance( obj.nested, MyBasicClass )
        assert obj.nested.str_prop == 'random string'
        assert obj.nested.int_prop == 4321

    def test_deserialize_enforce( self ):
        """
        test deserialization enforcing field type

        expect an error to be thrown on deserialization because the nested
        field is of the incorrect type

        :return:
        """
        body = {
            '_type': 'MyComplexClass',
            'prop': 'really cool property',
            'nested': {
                '_type': 'MyBasicClassWithLists',
                'str_prop': 'random string',
                'int_prop': 4321
            }
        }

        obj = MyTypedComplexClass()
        with pytest.raises( ValueError ):
            obj.deserialize( body )


class TestPrimitiveList( object ):
    """
    test case for serialization of basic lists of primitive strings and integers
    """

    def test_serialize( self ):
        """
        test serialization

        expect list within a standard field to function as standard list object
        and to dump up-to-date list of all primitive values

        :return:
        """
        obj = MyBasicClassWithLists()
        obj.str_list_prop = ['hello', 'world']
        obj.int_list_prop = [0, 1, 2, 3, 4]
        obj.str_list_prop.append( '!' )
        obj.int_list_prop.append( 5 )
        body = obj.serialize()

        assert body['_type'] == 'MyBasicClassWithLists'
        assert body['str_list_prop'] == ['hello', 'world', '!']
        assert body['int_list_prop'] == [0, 1, 2, 3, 4, 5]

    def test_deserialize( self ):
        """
        test deserialization

        expect json list of primitives to be loaded properly into
        serializable object

        :return:
        """
        body = {
            '_type': 'MyBasicClassWithLists',
            'str_list_prop': ['my', 'awesome', 'list', 'of', 'strings'],
            'int_list_prop': [9001, 9002, 9003]
        }

        obj = MyBasicClassWithLists()
        obj.deserialize( body )

        assert isinstance( obj, MyBasicClassWithLists )
        assert obj.str_list_prop == ['my', 'awesome', 'list', 'of', 'strings']
        assert obj.int_list_prop == [9001, 9002, 9003]

    def test_serialize_deep_copy( self ):
        """
        test serialization

        expect modification to original list to have no effect on
        serialized json body

        :return:
        """
        obj = MyBasicClassWithLists()
        obj.str_list_prop = ['hello', 'world']
        obj.int_list_prop = [0, 1, 2, 3, 4]
        body = obj.serialize()

        obj.str_list_prop.append( '!' )
        obj.int_list_prop.append( 5 )

        assert body['_type'] == 'MyBasicClassWithLists'
        assert body['str_list_prop'] == ['hello', 'world']
        assert body['int_list_prop'] == [0, 1, 2, 3, 4]

    def test_deserialize_deep_copy( self ):
        """
        test deserialization

        expect modification to original json list of primitives to
        have not effect on loaded serializable object

        :return:
        """
        body = {
            '_type': 'MyBasicClassWithLists',
            'str_list_prop': ['my', 'awesome', 'list', 'of', 'strings'],
            'int_list_prop': [9001, 9002, 9003]
        }

        obj = MyBasicClassWithLists()
        obj.deserialize( body )

        body['str_list_prop'].pop()
        body['int_list_prop'].pop()

        assert isinstance( obj, MyBasicClassWithLists )
        assert obj.str_list_prop == ['my', 'awesome', 'list', 'of', 'strings']
        assert obj.int_list_prop == [9001, 9002, 9003]


class TestNestedList( object ):
    """
    test case for model containing a list of nested serializable objects
    """

    def test_serializable( self ):
        """
        test serialization

        expect all nested instances of MyBasicClass to populate a list
        in json body of MyOtherComplexClass

        :return:
        """
        obj = MyOtherComplexClass()
        obj.str_prop = 'object name'
        obj.nested_list_prop = []

        nested_strings = ['some string', 'another string', 'one more string']
        nested_ints = [101, 102, 103]

        for s, n in zip( nested_strings, nested_ints ):
            temp = MyBasicClass()
            temp.str_prop = s
            temp.int_prop = n
            obj.nested_list_prop.append( temp )

        body = obj.serialize()

        assert body['_type'] == 'MyOtherComplexClass'
        assert body['str_prop'] == 'object name'
        assert len( body['nested_list_prop'] ) == 3
        for i, nested_body in enumerate( body['nested_list_prop'] ):
            assert nested_body['_type'] == 'MyBasicClass'
            assert nested_body['str_prop'] == nested_strings[i]
            assert nested_body['int_prop'] == nested_ints[i]

    def test_deserialize( self ):
        """
        test deserialization

        expect list of nested json objects to be deserialized into a list
        of MyBasicClass objects that is a member of MyComplexClass

        :return:
        """
        body = {
            '_type': 'MyOtherComplexClass',
            'str_prop': 'really great string property',
            'nested_list_prop': []
        }
        nested_strings = ['some string', 'another string', 'one more string']
        nested_ints = [101, 102, 103]

        for s, n in zip( nested_strings, nested_ints ):
            body['nested_list_prop'].append(
                {
                    '_type': 'MyBasicClass',
                    'str_prop': s,
                    'int_prop': n
                }
            )

        obj = MyOtherComplexClass()
        obj.deserialize( body )

        assert isinstance( obj, MyOtherComplexClass )
        assert obj.str_prop == 'really great string property'
        assert len( obj.nested_list_prop ) == 3
        for i, nested_obj in enumerate( obj.nested_list_prop ):
            assert isinstance( nested_obj, MyBasicClass )
            assert nested_obj.str_prop == nested_strings[i]
            assert nested_obj.int_prop == nested_ints[i]

    def test_deserialize_typed( self ):
        """
        test deserialization without _type field

        expect list of nested json objects to be deserialized into a list
        of MyBasicClass objects that is a member of MyComplexClass, even without
        _type field specified

        :return:
        """
        body = {
            '_type': 'MyOtherTypedComplexClass',
            'str_prop': 'really great string property',
            'nested_list_prop': []
        }
        nested_strings = ['some string', 'another string', 'one more string']
        nested_ints = [101, 102, 103]

        for s, n in zip( nested_strings, nested_ints ):
            body['nested_list_prop'].append(
                {
                    'str_prop': s,
                    'int_prop': n
                }
            )

        obj = MyOtherTypedComplexClass()
        obj.deserialize( body )

        assert isinstance( obj, MyOtherTypedComplexClass )
        assert obj.str_prop == 'really great string property'
        assert len( obj.nested_list_prop ) == 3
        for i, nested_obj in enumerate( obj.nested_list_prop ):
            assert isinstance( nested_obj, MyBasicClass )
            assert nested_obj.str_prop == nested_strings[i]
            assert nested_obj.int_prop == nested_ints[i]


class TestFieldOptionals( object ):
    """
    test case for optional params to field arguments
    """

    def test_serialize_default( self ):
        """
        test serialization

        expect default value to be serialized for unset str_prop, and
        int_prop to be serialized under key int_prop_named

        :return:
        """
        obj = MyClassWithFieldOptionals()
        obj.int_prop = 99

        assert obj.str_prop == 'default_val'

        body = obj.serialize()

        assert body['_type'] == 'MyClassWithFieldOptionals'
        assert body['str_prop'] == 'default_val'
        assert body['int_prop_named'] == 99

    def test_deserialize_default( self ):
        """
        test deserialization

        expect default value to be loaded into str_prop if not specified, and
        int_prop_named to be deserialized into int_prop

        :return:
        """
        body = {
            '_type': 'MySubClass',
            'int_prop_named': 99
        }

        obj = MyClassWithFieldOptionals()
        obj.deserialize( body )

        assert isinstance( obj, MyClassWithFieldOptionals )
        assert obj.str_prop == 'default_val'
        assert obj.int_prop == 99
