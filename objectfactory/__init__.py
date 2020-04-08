"""
objectfactory
"""

# do imports
from .serializable import Serializable
from .factory import Factory, register_class, create_object
from .field import Field, Nested, List

__version__ = '0.0.3'
