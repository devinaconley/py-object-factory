"""
objectfactory
"""

# do imports
from .serializable import Serializable, Field
from .factory import Factory as _Factory
from .field import Nested, List

# create factory aliases
register_class = _Factory.register_class
create_object = _Factory.create_object

__version__ = '0.0.2'
