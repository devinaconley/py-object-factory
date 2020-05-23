"""
field module

implements serializable fields
"""

# lib
from copy import deepcopy
import marshmallow

# src
from .base import FieldABC
from .factory import create_object


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

    def serialize( self, instance, include_type=True ):
        """
        accessor to be called during serialization

        :param instance:
        :param include_type:
        :return:
        """
        return getattr( deepcopy( instance ), self._key, self._default )

    def deserialize( self, instance, value ):
        """
        setter to be called during deserialization

        :param instance:
        :param value:
        :return:
        """
        setattr( instance, self._key, deepcopy( value ) )

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

    def serialize( self, instance, include_type=True ):
        """
        accessor to be called during serialization

        serialize() is called recursively on the nested object

        :param instance:
        :param include_type:
        :return:
        """
        obj = getattr( instance, self._key, self._default )
        if obj is None:
            return None
        return obj.serialize( include_type=include_type )

    def deserialize( self, instance, value ):
        """
        setter to be called during deserialization

        factory is used to create a nested object from json body

        :param instance:
        :param value:
        :return:
        """
        if value is None:
            return

        if '_type' in value:
            obj = create_object( value )
            if self._field_type and not isinstance( obj, self._field_type ):
                raise ValueError(
                    '{} is not an instance of type: {}'.format(
                        type( obj ).__name__, self._field_type.__name__ )
                )
        elif self._field_type:
            obj = self._field_type()
            obj.deserialize( value )
        else:
            raise ValueError( 'Cannot infer type information' )

        setattr( instance, self._key, obj )


class List( Field ):
    """
    field type for list of serializable objects
    """

    def __init__( self, default=None, name=None, field_type=None ):
        if default is None:
            default = []
        super().__init__( default=default, name=name, field_type=field_type )

    def serialize( self, instance, include_type=True ):
        """
        accessor to be called during serialization

        iterate across list and call serialize() recursively on each object

        :param instance:
        :param include_type:
        :return:
        """
        lst = []
        for obj in getattr( instance, self._key, self._default ):
            lst.append( obj.serialize( include_type=include_type ) )
        return lst

    def deserialize( self, instance, value ):
        """
        setter to be called during deserialization

        factory is used to create each serialized json object in list

        :param instance:
        :param value:
        :return:
        """
        lst = []
        for body in value:
            if '_type' in body:
                obj = create_object( body )
                if self._field_type and not isinstance( obj, self._field_type ):
                    raise ValueError(
                        '{} is not an instance of type: {}'.format(
                            type( obj ).__name__, self._field_type.__name__ )
                    )
            elif self._field_type:
                obj = self._field_type()
                obj.deserialize( body )
            else:
                raise ValueError( 'Cannot infer type information' )
            lst.append( obj )
        setattr( instance, self._key, lst )
