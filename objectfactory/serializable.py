"""
serializable module

implements base abstract class, metaclass, and base field class for serializable objects
"""

# lib
import abc

# src
from .base import FieldABC, SerializableABC


class Meta( abc.ABCMeta ):
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
        obj = abc.ABCMeta.__new__( mcs, name, bases, attributes )

        # init and collect serializable fields of parents
        fields = {}
        for base in bases:
            fields.update( getattr( base, '_fields', {} ) )

        # populate with all serializable class descriptors
        for name, attr in attributes.items():
            if isinstance( attr, FieldABC ):
                if attr._name is None:
                    attr._name = name
                attr._key = '_' + attr._name  # define key that descriptor will use to access data
                fields[name] = attr

        setattr( obj, '_fields', fields )
        return obj


class Serializable( SerializableABC, metaclass=Meta ):
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

    def serialize( self, include_type: bool = True, use_full_type: bool = True ) -> dict:
        """
        serialize model to JSON

        :param include_type: if true, type information will be included in body
        :param use_full_type: if true, the fully qualified path with be specified in body
        :return:
        :rtype dict
        """
        body = {}
        if include_type:
            if use_full_type:
                body['_type'] = self.__class__.__module__ + '.' + self.__class__.__name__
            else:
                body['_type'] = self.__class__.__name__

        for _, attr in self._fields.items():
            body[attr._name] = attr.serialize( self, include_type=include_type )

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
            attr.deserialize( self, body[attr._name] )
