"""
field module

implements serializable fields
"""

# src
from .serializable import Field
from .factory import Factory


class Nested( Field ):
    """
    field type for nested serializable object
    """

    def serialize_field( self, instance, deserializable=True ):
        """
        accessor to be called during serialization

        serialize() is called recursively on the nested object

        :param instance:
        :param deserializable:
        :return:
        """
        obj = getattr( instance, self._key, self._default )
        if obj is None:
            return None
        return obj.serialize( deserializable=deserializable )

    def deserialize_field( self, instance, value ):
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
            obj = Factory.create_object( value )
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

    def serialize_field( self, instance, deserializable=True ):
        """
        accessor to be called during serialization

        iterate across list and call serialize() recursively on each object

        :param instance:
        :param deserializable:
        :return:
        """
        lst = []
        for obj in getattr( instance, self._key, self._default ):
            lst.append( obj.serialize( deserializable=deserializable ) )
        return lst

    def deserialize_field( self, instance, value ):
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
                obj = Factory.create_object( body )
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
