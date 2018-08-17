"""
module for testing functionality of serializable factory, objects and fields
"""

# src
from objectfactory.serializable import Factory, Serializable, Field, Nested, List


@Factory.register_class
class MyBasicClass( Serializable ):
    """
    basic class to be used for testing serialization
    """
    str_prop = Field()
    int_prop = Field()


@Factory.register_class
class MyBasicClassWithLists( Serializable ):
    """
    basic class to be used for testing serialization of primitive lists
    """
    str_list_prop = Field()
    int_list_prop = Field()


@Factory.register_class
class MySubClass( MyBasicClass ):
    """
    sub class to be used for testing inheritance and serialization
    """
    int_prop = Field()
    str_prop_sub = Field()


@Factory.register_class
class MyComplexClass( Serializable ):
    """
    complex class to test hierarchical serialization
    """
    nested = Nested( MyBasicClass )
    prop = Field()


@Factory.register_class
class MyOtherComplexClass( Serializable ):
    """
    complex class to test list serialization
    """
    str_prop = Field()
    nested_list_prop = List()


@Factory.register_class
class MyClassWithFieldOptionals( Serializable ):
    """
    complex class to test list serialization
    """
    str_prop = Field( default='default_val' )
    int_prop = Field( name='int_prop_named' )


class TestFactory( object ):
    """
    test case for serializable factory
    """

    def test_register_class( self ):
        """
        validate register_class method

        MyTestClass should be registered
        :return:
        """
        assert 'MyBasicClass' in Factory.registry
        assert 'MyBasicClassWithLists' in Factory.registry
        assert 'MySubClass' in Factory.registry
        assert 'MyComplexClass' in Factory.registry
        assert 'MyOtherComplexClass' in Factory.registry

    def test_create_object( self ):
        """
        validate create object method
        :return:
        """
        body = {
            '_type': 'MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        obj = Factory.create_object( body )

        assert isinstance( obj, MyBasicClass )
        assert obj.str_prop == 'somestring'
        assert obj.int_prop == 42


class TestSerializable( object ):
    """
    test case for basic serializable object with primitive fields
    """

    def test_serialize( self ):
        """
        test serialization

        :return:
        """
        obj = MyBasicClass()
        obj.str_prop = 'my awesome string'
        obj.int_prop = 1234
        body = obj.serialize()

        assert body['_type'] == 'MyBasicClass'
        assert body['str_prop'] == 'my awesome string'
        assert body['int_prop'] == 1234

    def test_deserialize( self ):
        """
        test deserialization

        :return:
        """
        body = {
            '_type': 'MyBasicClass',
            'str_prop': 'another great string',
            'int_prop': 9001
        }

        obj = MyBasicClass()
        obj.deserialize( body )

        assert isinstance( obj, MyBasicClass )
        assert obj.str_prop == 'another great string'
        assert obj.int_prop == 9001

    def test_multiple( self ):
        """
        test deserializing multiple objects of same class

        validate there is no conflict in values of class level descriptors

        :return:
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
        obj1.deserialize( body1 )
        obj2 = MyBasicClass()
        obj2.deserialize( body2 )

        assert isinstance( obj1, MyBasicClass )
        assert obj1.str_prop == 'string1'
        assert obj1.int_prop == 9001

        assert isinstance( obj2, MyBasicClass )
        assert obj2.str_prop == 'string2'
        assert obj2.int_prop == 9002

    def test_init_keywords( self ):
        """
        test initializing class with keywords based on fields

        expect any fields to passable as a keyword arg to init

        :return:
        """
        obj = MyBasicClass(
            str_prop='some string',
            int_prop=12
        )

        assert obj.str_prop == 'some string'
        assert obj.int_prop == 12


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


class TestSubClass( object ):
    """
    test case for sub-classing another serializable model
    """

    def test_serialize( self ):
        """
        test serialization

        expect members of both parent and sub-class to be serialized, _type string
        should be MySubClass, and override should not cause conflict

        :return:
        """
        obj = MySubClass()
        obj.str_prop = 'parent_class_string'
        obj.int_prop = 99
        obj.str_prop_sub = 'sub_class_string'

        body = obj.serialize()

        assert body['_type'] == 'MySubClass'
        assert body['str_prop'] == 'parent_class_string'
        assert body['int_prop'] == 99
        assert body['str_prop_sub'] == 'sub_class_string'

    def test_deserialize( self ):
        """
        test deserialization

        expect both parent and sub-class members to be properly loaded, obj type
        should be MySubClass, and override should not cause conflict

        :return:
        """
        body = {
            '_type': 'MySubClass',
            'str_prop': 'parent_class_string',
            'int_prop': 99,
            'str_prop_sub': 'sub_class_string'
        }

        obj = MySubClass()
        obj.deserialize( body )

        assert isinstance( obj, MySubClass )
        assert obj.str_prop == 'parent_class_string'
        assert obj.int_prop == 99
        assert obj.str_prop_sub == 'sub_class_string'


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
