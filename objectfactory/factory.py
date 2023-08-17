"""
factory module

implements serializable object factory
"""
# lib
from typing import Type, TypeVar

# src
from .serializable import Serializable

# type var for hinting from generic function
T = TypeVar('T', bound=Serializable)


class Factory(object):
    """
    factory class for registering and creating serializable objects
    """

    def __init__(self, name):
        self.name = name
        self.registry = {}

    def register(self, serializable: Serializable):
        """
        decorator to register class with factory

        :param serializable: serializable object class
        :return: registered class
        """
        self.registry[serializable.__module__ + '.' + serializable.__name__] = serializable
        self.registry[serializable.__name__] = serializable
        return serializable

    def create(self, body: dict, object_type: Type[T] = Serializable) -> T:
        """
        create object from dictionary

        :param body: serialized object data
        :param object_type: (optional) specified object type
        :raises TypeError: if the object is not an instance of the specified type
        :return: deserialized object of specified type
        """
        obj = None
        try:
            obj = self.registry[body['_type']]()
        except KeyError:
            pass
        if obj is None:
            try:
                obj = self.registry[body['_type'].split('.')[-1]]()
            except KeyError:
                pass
        if obj is None:
            raise ValueError(
                'Object type {} not found in factory registry'.format(body['_type'])
            )

        if not isinstance(obj, object_type):
            raise TypeError(
                'Object type {} is not a {}'.format(
                    type(obj).__name__,
                    object_type.__name__
                )
            )

        obj.deserialize(body)
        return obj


# global registry
_global_factory = Factory('global')


def create(body: dict, object_type: Type[T] = Serializable) -> T:
    """
    create object from dictionary with the global factory

    :param body: serialized object data
    :param object_type: (optional) specified object type
    :raises TypeError: if the object is not an instance of the specified type
    :return: deserialized object of specified type
    """
    return _global_factory.create(body, object_type=object_type)


def register(serializable: Serializable):
    """
    decorator to register class with the global factory

    :param serializable: serializable object class
    :return: registered class
    """
    return _global_factory.register(serializable)
