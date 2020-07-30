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
            return getattr( instance, self._key )
        except AttributeError:
            # lazily create copy of default
            setattr( instance, self._key, deepcopy( self._default ) )
            return getattr( instance, self._key )

    def __set__( self, instance, value ):
        setattr( instance, self._key, value )

    def marshmallow( self ):
        """
        create marshmallow field

        :return:
        """
        return marshmallow.fields.Field(
            data_key=self._name,
            default=self._default
        )


class Integer( Field ):
    """
    field type for integer
    """

    def marshmallow( self ):
        return marshmallow.fields.Integer(
            data_key=self._name,
            default=self._default
        )


class String( Field ):
    """
    field type for string
    """

    def marshmallow( self ):
        return marshmallow.fields.String(
            data_key=self._name,
            default=self._default
        )


class Nested( Field ):
    """
    field type for nested serializable object
    """

    def __init__( self, default=None, name=None, field_type=None ):
        super().__init__( default=default, name=name )
        self._field_type = field_type

    def marshmallow( self ):
        return NestedFactoryField(
            field_type=self._field_type,
            data_key=self._name,
            default=self._default
        )


class List( Field ):
    """
    field type for list of serializable objects
    """

    def __init__( self, default=None, name=None, field_type=None ):
        if default is None:
            default = []
        super().__init__( default=default, name=name )
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

        return marshmallow.fields.List( cls )
