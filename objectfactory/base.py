"""
base module

implements abstract base classes for objectfactory
"""

from abc import ABC, abstractmethod


class FieldABC( ABC ):
    """
    abstract base class for serializable field
    """

    def __init__( self, default=None, name=None, field_type=None ):
        self._name = name
        self._key = None  # note: this will be set from parent metaclass __new__
        self._default = default
        self._field_type = field_type

    @abstractmethod
    def __get__( self, instance, owner ):
        pass

    @abstractmethod
    def __set__( self, instance, value ):
        pass

    @abstractmethod
    def serialize( self, instance, include_type: bool = True ):
        pass

    @abstractmethod
    def deserialize( self, instance, value ):
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
