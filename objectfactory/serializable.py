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

    def __new__( mcs, name, bases, attributes, schema=None ):
        """
        collect and register all field descriptors for the new serializable object

        :param name:
        :param bases:
        :param attributes:
        :param schema:
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
                if attr._key is None:
                    attr._key = attr_name
                attr._attr_key = '_' + attr_name  # define key that descriptor will use to access data
                fields[attr_name] = attr

        # generate marshmallow schema
        if schema is None:
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


class Serializable( SerializableABC, metaclass=Meta, schema=None ):
    """
    base abstract class for serializable objects
    """
    _fields = None
    _schema = None

    @classmethod
    def from_kwargs( cls, **kwargs ):
        """
        constructor to set field data by keyword args

        :param kwargs: keyword arguments by field
        :return: new instance of serializable object
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

        :param body: dictionary
        :return: new instance of serializable object
        """
        obj = cls()
        obj.deserialize( body )

        return obj

    def serialize( self, include_type: bool = True, use_full_type: bool = True ) -> dict:
        """
        serialize model to dictionary

        :param include_type: if true, type information will be included in body
        :param use_full_type: if true, the fully qualified path with be specified in body
        :return: serialized object as dict
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

    def deserialize( self, body: dict ):
        """
        deserialize model from dictionary

        :param body: serialized data to load into object
        """
        data = self._schema().load( body, unknown=marshmallow.EXCLUDE )
        for name, attr in self._fields.items():
            if attr._key not in body:
                continue
            if name not in data:
                continue
            setattr( self, name, data[name] )
