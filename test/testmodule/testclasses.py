"""
module to implement various dummy classes for use during testing
"""

# src
from objectfactory import register, Serializable, Field, Nested, List


@register
class MyBasicClass(Serializable):
    """
    basic class to be used for testing serialization
    """
    str_prop = Field()
    int_prop = Field()


@register
class MySubClass(MyBasicClass):
    """
    sub class to be used for testing inheritance and serialization
    """
    int_prop = Field()
    str_prop_sub = Field()


@register
class MyComplexClass(Serializable):
    """
    complex class to test hierarchical serialization
    """
    nested = Nested(MyBasicClass)
    prop = Field()
