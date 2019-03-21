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
        obj = Factory.create_object( value )
        setattr( instance, self._key, obj )


class List( Field ):
    """
    field type for list of serializable objects
    """

    def __init__( self, default=None ):
        if default is None:
            default = []
        super().__init__( default )

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
            lst.append( Factory.create_object( body ) )
        setattr( instance, self._key, lst )
