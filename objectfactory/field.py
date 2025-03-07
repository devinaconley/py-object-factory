"""
field module

implements serializable fields
"""

# lib
from copy import deepcopy
import marshmallow

# src
from .base import FieldABC, SerializableABC
from .factory import create
from .nested import NestedFactoryField


class Field(FieldABC):
    """
    base class for serializable field

    this is a class level descriptor for abstracting access to fields of
    serializable objects
    """

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self._attr_key)
        except AttributeError:
            # lazily create copy of default
            setattr(instance, self._attr_key, deepcopy(self._default))
            return getattr(instance, self._attr_key)

    def __set__(self, instance, value):
        setattr(instance, self._attr_key, value)

    def marshmallow(self):
        return marshmallow.fields.Raw(
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none
        )


class Integer(Field):
    """
    serializable field for integer data
    """

    def marshmallow(self):
        return marshmallow.fields.Integer(
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none
        )


class String(Field):
    """
    serializable field for string data
    """

    def marshmallow(self):
        return marshmallow.fields.String(
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none
        )


class Boolean(Field):
    """
    serializable field for boolean data
    """

    def marshmallow(self):
        return marshmallow.fields.Boolean(
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none
        )


class Float(Field):
    """
    serializable field for float data
    """

    def marshmallow(self):
        return marshmallow.fields.Float(
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none
        )


class DateTime(Field):
    """
    serializable field for datetime data
    """

    def __init__(
        self,
        default=None,
        key=None,
        date_format=None,
        required=False,
        allow_none=True
    ):
        """
        :param default: default value for field if unset
        :param key: dictionary key to use for field serialization
        :param date_format: date format to use (defaults to iso)
        :param required: whether this field is required to deserialize an object
        :param allow_none: whether null should be considered a valid value
        """
        super().__init__(default=default, key=key, required=required, allow_none=allow_none)
        self._date_format = date_format

    def marshmallow(self):
        return marshmallow.fields.DateTime(
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none,
            format=self._date_format
        )


class Enum(Field):
    """
    serializable field for enumerated data
    """

    def __init__(
        self,
        enum,
        default=None,
        key=None,
        required=False,
        allow_none=True,
        by_value=False,
    ):
        """
        :param enum: enum type for field validation
        :param default: default value for field if unset
        :param key: dictionary key to use for field serialization
        :param required: whether this field is required to deserialize an object
        :param allow_none: whether null should be considered a valid value
        :param by_value: whether to serialize by value or by symbol
        """
        super().__init__(default=default, key=key, required=required, allow_none=allow_none)
        self._enum = enum
        self._by_value = by_value

    def marshmallow(self):
        return marshmallow.fields.Enum(
            self._enum,
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none,
            by_value=self._by_value
        )


class Nested(Field):
    """
    field type for nested serializable object
    """

    def __init__(
        self,
        default=None,
        key=None,
        field_type=None,
        required=False,
        allow_none=True
    ):
        """
        :param default: default value for field if unset
        :param key: dictionary key to use for field serialization
        :param field_type: specified type for nested object
        :param required: whether this field is required to deserialize an object
        :param allow_none: whether null should be considered a valid value
        """
        super().__init__(default=default, key=key, required=required, allow_none=allow_none)
        self._field_type = field_type

    def marshmallow(self):
        return NestedFactoryField(
            field_type=self._field_type,
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none
        )


class List(Field):
    """
    field type for list of serializable objects
    """

    def __init__(
        self,
        default=None,
        key=None,
        field_type=None,
        required=False,
        allow_none=True
    ):
        """
        :param default: default value for field if unset
        :param key: dictionary key to use for field serialization
        :param field_type: specified type for list of nested objects
        :param required: whether this field is required to deserialize an object
        :param allow_none: whether null should be considered a valid value
        """
        if default is None:
            default = []
        super().__init__(default=default, key=key, required=required, allow_none=allow_none)
        self._field_type = field_type

    def marshmallow(self):
        if self._field_type is None or issubclass(self._field_type, SerializableABC):
            cls = NestedFactoryField(field_type=self._field_type)
        elif issubclass(self._field_type, FieldABC):
            cls = self._field_type().marshmallow()
        elif issubclass(self._field_type, marshmallow.fields.FieldABC):
            cls = self._field_type
        else:
            raise ValueError('Invalid field type in List: {}'.format(self._field_type))

        return marshmallow.fields.List(
            cls,
            data_key=self._key,
            required=self._required,
            allow_none=self._allow_none
        )
