"""
serializable module

implements base abstract class, metaclass, and base field class for serializable objects
"""

# lib
from copy import deepcopy


class Field( object ):
    """
    base class for serializable field

    this is a class level descriptor for abstracting access to fields of
    serializable objects
    """

    def __init__( self, default=None, name=None, field_type=None ):
        self._name = name
        self._key = None  # note: this will be set from parent metaclass __new__
        self._default = default
        self._field_type = field_type

    def __get__( self, instance, owner ):
        try:
            return getattr( instance, self._key )
        except AttributeError:
            # lazily create copy of default
            setattr( instance, self._key, deepcopy( self._default ) )
            return getattr( instance, self._key )

    def __set__( self, instance, value ):
        setattr( instance, self._key, value )

    def serialize_field( self, instance, deserializable=True ):
        """
        accessor to be called during serialization

        :param instance:
        :param deserializable:
        :return:
        """
        return getattr( deepcopy( instance ), self._key, self._default )

    def deserialize_field( self, instance, value ):
        """
        setter to be called during deserialization

        :param instance:
        :param value:
        :return:
        """
        setattr( instance, self._key, deepcopy( value ) )


class Meta( type ):
    """
    metaclass for serializable classes

    this is a metaclass to be used for collecting relevant field information when
    defining a new serializable class
    """

    def __new__( mcs, name, bases, attributes ):
        """
        collect and register all field descriptors for the new serializable object

        :param name:
        :param bases:
        :param attributes:
        :return:
        """
        obj = type.__new__( mcs, name, bases, attributes )

        # init and collect serializable fields of parents
        fields = {}
        for base in bases:
            fields.update( getattr( base, '_fields', {} ) )

        # populate with all serializable class descriptors
        for name, attr in attributes.items():
            if isinstance( attr, Field ):
                if attr._name is None:
                    attr._name = name
                attr._key = '_' + attr._name  # define key that descriptor will use to access data
                fields[name] = attr

        setattr( obj, '_fields', fields )
        return obj


class Serializable( object, metaclass=Meta ):
    """
    base abstract class for serializable objects
    """
    _fields = {}

    @classmethod
    def from_kwargs( cls, **kwargs ):
        """
        accept any fields as keyword args to constructor
        """
        obj = cls()
        for key, val in kwargs.items():
            if key in obj._fields:
                obj._fields[key].__set__( obj, val )

        return obj

    def serialize( self, deserializable: bool = True, use_full_type: bool = True ) -> dict:
        """
        serialize model to JSON

        :param deserializable: if true, type information will be included in body
        :param use_full_type: if true, the fully qualified path with be specified in body
        :return:
        :rtype dict
        """
        body = {}
        if deserializable:
            if use_full_type:
                body['_type'] = self.__class__.__module__ + '.' + self.__class__.__name__
            else:
                body['_type'] = self.__class__.__name__

        for _, attr in self._fields.items():
            body[attr._name] = attr.serialize_field( self, deserializable=deserializable )

        return body

    def deserialize( self, body: dict ):
        """
        deserialize model from JSON

        :param body:
        :return:
        """
        for _, attr in self._fields.items():
            if attr._name not in body:
                continue  # accept default
            attr.deserialize_field( self, body[attr._name] )
