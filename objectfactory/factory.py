"""
factory module

implements serializable object factory
"""

# src
from .serializable import Serializable


class Factory( object ):
    """
    factory class for registering and creating serializable objects
    """

    registry = {}

    @classmethod
    def register_class( cls, serializable: Serializable ):
        """
        register class with factory

        :param name:
        :param serializable:
        :return:
        """
        cls.registry[serializable.__name__] = serializable
        return serializable

    @classmethod
    def create_object( cls, body: dict ) -> Serializable:
        """
        create object from JSON dictionary

        :param body:
        :return:
        """
        obj = cls.registry[body['_type']]()
        obj.deserialize( body )
        return obj
