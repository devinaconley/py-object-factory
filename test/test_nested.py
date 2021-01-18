"""
module for testing serializable Nested field
"""

# lib
import pytest
import marshmallow

# src
import objectfactory
from objectfactory import Serializable, Nested, String, register
from objectfactory.nested import NestedFactoryField


class TestNested( object ):
    """
    test case for nested object field type
    """

    def setup_method( self, _ ):
        """
        prepare for each test
        """
        objectfactory.factory._global_factory.registry.clear()

    def test_definition( self ):
        """
        test definition of class with nested field

        expect field to to be collected, registered, and included
        in schema creation
        """

        class MyTestClass( Serializable ):
            nested = Nested()

        assert isinstance( MyTestClass._fields, dict )
        assert len( MyTestClass._fields ) == 1
        assert 'nested' in MyTestClass._fields
        assert isinstance( MyTestClass._fields['nested'], Nested )

        schema = MyTestClass._schema
        assert issubclass( schema, marshmallow.Schema )
        assert len( schema._declared_fields ) == 1
        assert 'nested' in schema._declared_fields

        prop = schema._declared_fields['nested']
        assert isinstance( prop, NestedFactoryField )

    def test_serialize( self ):
        """
        test serialize

        expect nested object to be dumped to nested dict in json body
        """

        class MyNestedClass( Serializable ):
            str_prop = String()

        class MyTestClass( Serializable ):
            nested = Nested()

        obj = MyTestClass()
        obj.nested = MyNestedClass()
        obj.nested.str_prop = 'some string'

        body = obj.serialize()

        assert body['_type'] == 'test.test_nested.MyTestClass'
        assert isinstance( body['nested'], dict )
        assert body['nested']['_type'] == 'test.test_nested.MyNestedClass'
        assert body['nested']['str_prop'] == 'some string'

    def test_deserialize( self ):
        """
        test deserialization

        expect nested object to be created and data to be loaded
        """

        @register
        class MyNestedClass( Serializable ):
            str_prop = String()

        class MyTestClass( Serializable ):
            nested = Nested()

        body = {
            '_type': 'MyTestClass',
            'nested': {
                '_type': 'MyNestedClass',
                'str_prop': 'some string'
            }
        }

        obj = MyTestClass()
        obj.deserialize( body )

        assert isinstance( obj, MyTestClass )
        assert isinstance( obj.nested, MyNestedClass )
        assert obj.nested.str_prop == 'some string'

    def test_deserialize_typed( self ):
        """
        test deserialization with typed nested field

        expect nested object to be created and data to be loaded based
        on specified field type, despite lack of type info or registration
        """

        class MyNestedClass( Serializable ):
            str_prop = String()

        class MyTestClass( Serializable ):
            nested = Nested( field_type=MyNestedClass )

        body = {
            '_type': 'MyTestClass',
            'nested': {
                'str_prop': 'some string'
            }
        }

        obj = MyTestClass()
        obj.deserialize( body )

        assert isinstance( obj, MyTestClass )
        assert isinstance( obj.nested, MyNestedClass )
        assert obj.nested.str_prop == 'some string'

    def test_deserialize_enforce_typed( self ):
        """
        test deserialization enforcing field type

        expect an error to be thrown on deserialization because the nested
        field is of the incorrect type
        """

        @register
        class MyNestedClass( Serializable ):
            str_prop = String()

        @register
        class OtherClass( Serializable ):
            str_prop = String()

        class MyTestClass( Serializable ):
            nested = Nested( field_type=MyNestedClass )

        body = {
            '_type': 'MyTestClass',
            'nested': {
                '_type': 'OtherClass',
                'str_prop': 'some string',
            }
        }

        obj = MyTestClass()
        with pytest.raises( ValueError ):
            obj.deserialize( body )
