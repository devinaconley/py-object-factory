"""
base module

implements abstract base classes for objectfactory
"""

from abc import ABC, abstractmethod


class FieldABC(ABC):
    """
    abstract base class for serializable field
    """

    def __init__(self, default=None, key=None, required=False, allow_none=True):
        """
        :param default: default value for field if unset
        :param key: dictionary key to use for field serialization
        :param required: whether this field is required to deserialize an object
        :param allow_none: whether null should be considered a valid value
        """
        self._key = key
        self._attr_key = None  # note: this will be set from parent metaclass __new__
        self._default = default
        self._required = required
        self._allow_none = allow_none

    @abstractmethod
    def __get__(self, instance, owner):
        pass

    @abstractmethod
    def __set__(self, instance, value):
        pass

    @abstractmethod
    def marshmallow(self):
        """
        create generic marshmallow field to do actual serialization

        :return: associated marshmallow field
        """
        pass


class SerializableABC(ABC):
    """
    abstract base class for serializable object
    """

    @abstractmethod
    def serialize(self, include_type: bool = True, use_full_type: bool = True) -> dict:
        """
        serialize model to dictionary

        :param include_type: if true, type information will be included in body
        :param use_full_type: if true, the fully qualified path with be specified in body
        :return: serialized object as dict
        """
        pass

    @abstractmethod
    def deserialize(self, body: dict):
        """
        deserialize model from dictionary

        :param body: serialized data to load into object
        """
        pass
