"""
serializable module

implements base abstract class, metaclass, and base field class for serializable objects
"""

# lib
from abc import ABCMeta
import marshmallow

# src
from .base import FieldABC, SerializableABC


class Meta( ABCMeta ):
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
        obj = ABCMeta.__new__( mcs, name, bases, attributes )

        # init and collect serializable fields of parents
        fields = {}
        for base in bases:
            fields.update( getattr( base, '_fields', {} ) )

        # populate with all serializable class descriptors
        for attr_name, attr in attributes.items():
            if isinstance( attr, FieldABC ):
                if attr._name is None:
                    attr._name = attr_name
                attr._key = '_' + attr._name  # define key that descriptor will use to access data
                fields[attr_name] = attr

        # generate marshmallow schema
        marsh_fields = {
            attr_name: attr.marshmallow()
            for attr_name, attr in fields.items()
        }
        schema = marshmallow.Schema.from_dict(
            marsh_fields,
            name='_{}Schema'.format( name )
        )

        # set fields and schema
        setattr( obj, '_fields', fields )
        setattr( obj, '_schema', schema )
        return obj


class Serializable( SerializableABC, metaclass=Meta ):
    """
    base abstract class for serializable objects
    """
    _fields = None
    _schema = None

    @classmethod
    def from_kwargs( cls, **kwargs ):
        """
        constructor to accept any fields as keyword args
        """
        obj = cls()
        for key, val in kwargs.items():
            if key in obj._fields:
                obj._fields[key].__set__( obj, val )

        return obj

    @classmethod
    def from_dict( cls, body: dict ):
        """
        constructor to set data with dictionary
        """
        obj = cls()
        for key, val in body.items():
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

    def serialize_marsh( self, include_type: bool = True, use_full_type: bool = True ) -> dict:
        """
        dev method until marshmallow integration is complete

        :param include_type:
        :param use_full_type:
        :return:
        """
        self._serialize_kwargs = {
            'include_type': include_type,
            'use_full_type': use_full_type
        }

        body = self._schema().dump( self )
        if include_type:
            if use_full_type:
                body['_type'] = self.__class__.__module__ + '.' + self.__class__.__name__
            else:
                body['_type'] = self.__class__.__name__
        return body

    def deserialize_marsh( self, body: dict ):
        """
        dev method until marshmallow integration is complete

        :param body:
        :return:
        """
        data = self._schema().load( body, unknown=marshmallow.EXCLUDE )
        for name, attr in self._fields.items():
            if attr._name not in body:
                continue
            setattr( self, name, data[attr._name] )
