"""
module for testing functionality of serializable factory
"""

# lib
import pytest

# src
import objectfactory
from objectfactory.factory import _global_factory
from .testmodule.testclasses import MyBasicClass, MyComplexClass


class TestFactory(object):
    """
    test case for serializable factory
    """

    def test_register_class(self):
        """
        validate register_class method

        MyBasicClass should be registered
        """
        assert 'MyBasicClass' in _global_factory.registry
        assert 'test.testmodule.testclasses.MyBasicClass' in _global_factory.registry

    def test_create_object(self):
        """
        validate create object method

        expect object to be deserialized properly
        """
        body = {
            '_type': 'test.testmodule.testclasses.MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        obj = objectfactory.create(body)

        assert isinstance(obj, MyBasicClass)
        assert obj.str_prop == 'somestring'
        assert obj.int_prop == 42

    def test_create_object_short_type(self):
        """
        validate create object method without fully qualified path

        expect object to be deserialized properly
        """
        body = {
            '_type': 'MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        obj = objectfactory.create(body)

        assert isinstance(obj, MyBasicClass)
        assert obj.str_prop == 'somestring'
        assert obj.int_prop == 42

    def test_create_object_other_full_path(self):
        """
        validate create object method when full path is altered

        expect object to be deserialized properly based on last path element
        """
        body = {
            '_type': 'some.other.module.MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        obj = objectfactory.create(body)

        assert isinstance(obj, MyBasicClass)
        assert obj.str_prop == 'somestring'
        assert obj.int_prop == 42

    def test_create_object_unregistered(self):
        """
        validate create object method throws when unregistered

        expect ValueError to be raised indicating that the type is not registered
        """
        body = {
            '_type': 'MyClassThatDoesNotExist',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        with pytest.raises(ValueError, match=r'.*type MyClassThatDoesNotExist not found.*'):
            _ = objectfactory.create(body)

    def test_create_object_typed(self):
        """
        validate create object method when enforcing type

        expect object to be returned with full type hinting
        """
        body = {
            '_type': 'test.testmodule.testclasses.MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        obj = objectfactory.create(body, object_type=MyBasicClass)

        assert isinstance(obj, MyBasicClass)
        assert obj.str_prop == 'somestring'
        assert obj.int_prop == 42

    def test_create_object_typed_invalid(self):
        """
        validate create object method throws when type mismatch

        expect TypeError to be raised indicating a type mismatch
        """
        body = {
            '_type': 'test.testmodule.testclasses.MyBasicClass',
            'str_prop': 'somestring',
            'int_prop': 42,
        }
        with pytest.raises(
                TypeError,
                match=r'.*Object type MyBasicClass is not a MyComplexClass.*'
        ):
            _ = objectfactory.create(body, object_type=MyComplexClass)
