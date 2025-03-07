"""
factory module

implements serializable object factory
"""
# lib
from typing import Type, TypeVar

# src
from .base import SerializableABC

# type var for hinting from generic function
T = TypeVar('T', bound=SerializableABC)


class Factory(object):
    """
    factory class for registering and creating serializable objects
    """

    def __init__(self, name):
        self.name = name
        self.registry = {}

    def register(self, serializable: SerializableABC):
        """
        decorator to register class with factory

        :param serializable: serializable object class
        :return: registered class
        """
        self.registry[serializable.__module__ + '.' + serializable.__name__] = serializable
        self.registry[serializable.__name__] = serializable
        return serializable

    def create(self, body: dict, object_type: Type[T] = SerializableABC) -> T:
        """
        create object from dictionary

        :param body: serialized object data
        :param object_type: (optional) specified object type
        :raises TypeError: if the object is not an instance of the specified type
        :return: deserialized object of specified type
        """
        cls = None
        try:
            cls = self.registry[body['_type']]
        except KeyError:
            pass
        if cls is None:
            try:
                cls = self.registry[body['_type'].split('.')[-1]]
            except KeyError:
                pass
        if cls is None:
            raise ValueError(
                'Object type {} not found in factory registry'.format(body['_type'])
            )

        if not issubclass(cls, object_type):
            raise TypeError(f'Object type {cls.__name__} is not a {object_type.__name__}')
        obj = cls.from_dict(body)
        # obj.deserialize(body)
        return obj


# global registry
_global_factory = Factory('global')


def create(body: dict, object_type: Type[T] = SerializableABC) -> T:
    """
    create object from dictionary with the global factory

    :param body: serialized object data
    :param object_type: (optional) specified object type
    :raises TypeError: if the object is not an instance of the specified type
    :return: deserialized object of specified type
    """
    return _global_factory.create(body, object_type=object_type)


def register(serializable: SerializableABC):
    """
    decorator to register class with the global factory

    :param serializable: serializable object class
    :return: registered class
    """
    return _global_factory.register(serializable)
