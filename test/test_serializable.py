"""
module for testing functionality of serializable objects
"""

# src
from objectfactory import Factory, Serializable, Field


@Factory.register_class
class MyBasicClass( Serializable ):
    """
    basic class to be used for testing serialization
    """
    str_prop = Field()
    int_prop = Field()


@Factory.register_class
class MySubClass( MyBasicClass ):
    """
    sub class to be used for testing inheritance and serialization
    """
    int_prop = Field()
    str_prop_sub = Field()


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
