"""
base module

implements abstract base classes for objectfactory
"""

from abc import ABC, abstractmethod


class FieldABC( ABC ):
    """
    abstract base class for serializable field
    """

    def __init__( self, default=None, key=None, required=False ):
        """
        constructor for serializable field

        :param default: default value for field if unset
        :param key: dictionary key to use for field serialization
        :param required: whether this field is required to deserialize an object
        """
        self._key = key
        self._attr_key = None  # note: this will be set from parent metaclass __new__
        self._default = default
        self._required = required

    @abstractmethod
    def __get__( self, instance, owner ):
        pass

    @abstractmethod
    def __set__( self, instance, value ):
        pass

    @abstractmethod
    def marshmallow( self ):
        pass


class SerializableABC( ABC ):
    """
    abstract base class for serializable object
    """

    @abstractmethod
    def serialize( self, include_type: bool = True, use_full_type: bool = True ) -> dict:
        pass

    @abstractmethod
    def deserialize( self, body: dict ):
        pass
