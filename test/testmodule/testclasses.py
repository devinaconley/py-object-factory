"""
module to implement various dummy classes for use during testing
"""

# src
from objectfactory import register_class, Serializable, Field, Nested, List


@register_class
class MyBasicClass( Serializable ):
    """
    basic class to be used for testing serialization
    """
    str_prop = Field()
    int_prop = Field()


@register_class
class MySubClass( MyBasicClass ):
    """
    sub class to be used for testing inheritance and serialization
    """
    int_prop = Field()
    str_prop_sub = Field()


@register_class
class MyComplexClass( Serializable ):
    """
    complex class to test hierarchical serialization
    """
    nested = Nested( MyBasicClass )
    prop = Field()
