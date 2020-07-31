"""
field module

implements serializable fields
"""

# lib
from copy import deepcopy
import marshmallow

# src
from .base import FieldABC, SerializableABC
from .factory import create_object
from .nested import NestedFactoryField


class Field( FieldABC ):
    """
    base class for serializable field

    this is a class level descriptor for abstracting access to fields of
    serializable objects
    """

    def __get__( self, instance, owner ):
        try:
            return getattr( instance, self._attr_key )
        except AttributeError:
            # lazily create copy of default
            setattr( instance, self._attr_key, deepcopy( self._default ) )
            return getattr( instance, self._attr_key )

    def __set__( self, instance, value ):
        setattr( instance, self._attr_key, value )

    def marshmallow( self ):
        """
        create generic marshmallow field

        :return:
        """
        return marshmallow.fields.Field(
            data_key=self._key,
            default=self._default
        )


class Integer( Field ):
    """
    serializable field for integer data
    """

    def marshmallow( self ):
        return marshmallow.fields.Integer(
            data_key=self._key,
            default=self._default
        )


class String( Field ):
    """
    serializable field for string data
    """

    def marshmallow( self ):
        return marshmallow.fields.String(
            data_key=self._key,
            default=self._default
        )


class Boolean( Field ):
    """
    serializable field for boolean data
    """

    def marshmallow( self ):
        return marshmallow.fields.Boolean(
            data_key=self._key,
            default=self._default
        )


class Float( Field ):
    """
    serializable field for float data
    """

    def marshmallow( self ):
        return marshmallow.fields.Float(
            data_key=self._key,
            default=self._default
        )


class Nested( Field ):
    """
    field type for nested serializable object
    """

    def __init__( self, default=None, key=None, field_type=None ):
        super().__init__( default=default, key=key )
        self._field_type = field_type

    def marshmallow( self ):
        return NestedFactoryField(
            field_type=self._field_type,
            data_key=self._key,
            default=self._default
        )


class List( Field ):
    """
    field type for list of serializable objects
    """

    def __init__( self, default=None, key=None, field_type=None ):
        if default is None:
            default = []
        super().__init__( default=default, key=key )
        self._field_type = field_type

    def marshmallow( self ):
        if self._field_type is None or issubclass( self._field_type, SerializableABC ):
            cls = NestedFactoryField( field_type=self._field_type )
        elif issubclass( self._field_type, FieldABC ):
            cls = self._field_type().marshmallow()
        elif issubclass( self._field_type, marshmallow.fields.FieldABC ):
            cls = self._field_type
        else:
            raise ValueError( 'Invalid field type in List: {}'.format( self._field_type ) )

        return marshmallow.fields.List( cls, data_key=self._key )
