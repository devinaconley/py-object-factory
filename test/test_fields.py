"""
module for testing serializable List field
"""

# lib
import pytest

# src
from objectfactory import Serializable, Field, Nested, List, register_class
from objectfactory.factory import _global_factory


class TestFieldOptionals( object ):
    """
    test case for optional params to field arguments
    """

    def test_serialize_default( self ):
        """
        test serialization

        expect default value to be serialized for unset str_prop, and
        int_prop to be serialized under key int_prop_named
        """

        class MyTestClass( Serializable ):
            str_prop = Field( default='default_val' )

        obj = MyTestClass()

        assert obj.str_prop == 'default_val'

        body = obj.serialize()

        assert body['_type'] == 'test.test_fields.MyTestClass'
        assert body['str_prop'] == 'default_val'

    def test_deserialize_default( self ):
        """
        test deserialization

        expect default value to be loaded into str_prop if not specified, and
        int_prop_named to be deserialized into int_prop
        """

        class MyTestClass( Serializable ):
            str_prop = Field( default='default_val' )

        body = {
            '_type': 'MyTestClass'
        }

        obj = MyTestClass()
        obj.deserialize( body )

        assert isinstance( obj, MyTestClass )
        assert obj.str_prop == 'default_val'

    def test_serialize_named( self ):
        """
        test serialization

        expect int_prop to be serialized under key int_prop_named
        """

        class MyTestClass( Serializable ):
            int_prop = Field( name='int_prop_named' )

        obj = MyTestClass()
        obj.int_prop = 99

        body = obj.serialize()

        assert body['_type'] == 'test.test_fields.MyTestClass'
        assert body['int_prop_named'] == 99

    def test_deserialize_named( self ):
        """
        test deserialization

        expect int_prop_named to be deserialized into int_prop
        """

        class MyTestClass( Serializable ):
            int_prop = Field( name='int_prop_named' )

        body = {
            '_type': 'MyTestClass',
            'int_prop_named': 99
        }

        obj = MyTestClass()
        obj.deserialize( body )

        assert isinstance( obj, MyTestClass )
        assert obj.int_prop == 99
