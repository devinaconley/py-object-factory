"""
module for testing functionality of serializable factory
"""

# lib
import pytest

# src
from objectfactory import Factory
from .testmodule.testclasses import MyBasicClass


class TestFactory( object ):
    """
    test case for serializable factory
    """

    def test_register_class( self ):
        """
        validate register_class method

        MyBasicClass should be registered
        :return:
        """
        assert 'MyBasicClass' in Factory.registry
        assert 'test.testmodule.testclasses.MyBasicClass' in Factory.registry

    def test_create_object( self ):
        """
        validate create object method

        expect object to be deserialized properly
        :return:
        """
        body = {
            '_type': 'test.testmodule.testclasses.MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        obj = Factory.create_object( body )

        assert isinstance( obj, MyBasicClass )
        assert obj.str_prop == 'somestring'
        assert obj.int_prop == 42

    def test_create_object_short_type( self ):
        """
        validate create object method without fully qualified path

        expect object to be deserialized properly
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

    def test_create_object_other_full_path( self ):
        """
        validate create object method when full path is altered

        expect object to be deserialized properly based on last path element
        :return:
        """
        body = {
            '_type': 'some.other.module.MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        obj = Factory.create_object( body )

        assert isinstance( obj, MyBasicClass )
        assert obj.str_prop == 'somestring'
        assert obj.int_prop == 42

    def test_create_object_unregistered( self ):
        """
        validate create object method throws when unregistered

        expect object to be deserialized properly
        :return:
        """
        body = {
            '_type': 'MyClassThatDoesNotExist',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        with pytest.raises( ValueError, match=r'.*type MyClassThatDoesNotExist not found.*' ):
            obj = Factory.create_object( body )
