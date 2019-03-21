"""
module for testing functionality of serializable factory
"""

# src
from objectfactory import Factory
from .test_serializable import MyBasicClass


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
