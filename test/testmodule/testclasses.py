"""
module to implement various dummy classes for use during testing
"""

# src
from objectfactory import Factory, Serializable, Field, Nested, List


@Factory.register_class
class MyBasicClass( Serializable ):
    """
    basic class to be used for testing serialization
    """
    str_prop = Field()
    int_prop = Field()


@Factory.register_class
class MySubClass( MyBasicClass ):
    """
    sub class to be used for testing inheritance and serialization
    """
    int_prop = Field()
    str_prop_sub = Field()


@Factory.register_class
class MyBasicClassWithLists( Serializable ):
    """
    basic class to be used for testing serialization of primitive lists
    """
    str_list_prop = Field()
    int_list_prop = Field()


@Factory.register_class
class MyComplexClass( Serializable ):
    """
    complex class to test hierarchical serialization
    """
    nested = Nested( MyBasicClass )
    prop = Field()


@Factory.register_class
class MyOtherComplexClass( Serializable ):
    """
    complex class to test list serialization
    """
    str_prop = Field()
    nested_list_prop = List()


@Factory.register_class
class MyClassWithFieldOptionals( Serializable ):
    """
    complex class to test list serialization
    """
    str_prop = Field( default='default_val' )
    int_prop = Field( name='int_prop_named' )
