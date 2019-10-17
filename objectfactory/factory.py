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
        cls.registry[serializable.__module__ + '.' + serializable.__name__] = serializable
        cls.registry[serializable.__name__] = serializable
        return serializable

    @classmethod
    def create_object( cls, body: dict ) -> Serializable:
        """
        create object from JSON dictionary

        :param body:
        :return:
        """
        try:
            obj = cls.registry[body['_type']]()
            obj.deserialize( body )
            return obj
        except KeyError:
            pass
        try:
            obj = cls.registry[body['_type'].split( '.' )[-1]]()
            obj.deserialize( body )
            return obj
        except KeyError:
            pass
        raise ValueError( 'Object type {} not found in factory registry'.format( body['_type'] ) )
