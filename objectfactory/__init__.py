"""
objectfactory
"""

# do imports
from .serializable import Serializable
from .factory import Factory, register_class, create_object
from .field import Field, Nested, List, Integer, String

__version__ = '0.1.0b'
