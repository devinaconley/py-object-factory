"""
base module

implements abstract base classes for objectfactory
"""

import abc


class FieldABC( abc.ABC ):
    """
    abstract base class for serializable field
    """

    def __init__( self, default=None, name=None, field_type=None ):
        self._name = name
        self._key = None  # note: this will be set from parent metaclass __new__
        self._default = default
        self._field_type = field_type

    @abc.abstractmethod
    def __get__( self, instance, owner ):
        pass

    @abc.abstractmethod
    def __set__( self, instance, value ):
        pass

    @abc.abstractmethod
    def serialize( self, instance, include_type: bool = True ):
        pass

    @abc.abstractmethod
    def deserialize( self, instance, value ):
        pass


class SerializableABC( abc.ABC ):
    """
    abstract base class for serializable object
    """

    @abc.abstractmethod
    def serialize( self, include_type: bool = True, use_full_type: bool = True ) -> dict:
        pass

    @abc.abstractmethod
    def deserialize( self, body: dict ):
        pass
