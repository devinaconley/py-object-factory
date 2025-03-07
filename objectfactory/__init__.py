"""
objectfactory is a python package to easily implement the factory design pattern
for object creation, serialization, and polymorphism
"""

# do imports
from .serializable import Serializable
from .factory import Factory, register, create
from .field import Field, Nested, List, Integer, String, Boolean, Float, DateTime, Enum

__version__ = '0.1.0'
