"""
nested field

implements marshmallow field for objectfactory nested objects
"""

# lib
import marshmallow

# src
from .serializable import Serializable
from .factory import create


class NestedFactoryField(marshmallow.fields.Field):

    def __init__(self, field_type=None, **kwargs):
        super().__init__(**kwargs)
        self._field_type = field_type

    def _serialize(self, value, attr, obj, **kwargs):
        """
        dump serializable object within the interface of marshmallow field

        :param value:
        :param attr:
        :param obj:
        :param kwargs:
        :return:
        """
        if not isinstance(value, Serializable):
            return {}
        return value.serialize(**obj._serialize_kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        """
        create serializable object with factory through interface of marshmallow field

        :param value:
        :param attr:
        :param data:
        :param kwargs:
        :return:
        """
        if value is None:
            return

        if '_type' in value:
            obj = create(value)
            if self._field_type and not isinstance(obj, self._field_type):
                raise ValueError(
                    '{} is not an instance of type: {}'.format(
                        type(obj).__name__, self._field_type.__name__)
                )
        elif self._field_type:
            obj = self._field_type()
            obj.deserialize(value)
        else:
            raise ValueError('Cannot infer type information')

        return obj
