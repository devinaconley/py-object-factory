# py-object-factory

[![Build Status](https://travis-ci.org/devinaconley/py-object-factory.svg?branch=develop)](https://travis-ci.org/devinaconley/py-object-factory)
[![codecov](https://codecov.io/gh/devinaconley/py-object-factory/branch/develop/graph/badge.svg)](https://codecov.io/gh/devinaconley/py-object-factory)

**objectfactory** is a python package to easily implement the factory design pattern for object creation and serialization
- serialization schema inherent in class definition
- consistent interface to load many objects of arbitrary type
- serialize object to human-readable JSON format

## Example 
Simple **shapes** example:
```python
import objectfactory

@objectfactory.Factory.register_class
class Square( objectfactory.Serializable ):
    side = objectfactory.Field()

    def get_area( self ):
        return self.side * self.side

@objectfactory.Factory.register_class
class Triangle( objectfactory.Serializable ):
    base = objectfactory.Field()
    height = objectfactory.Field()

    def get_area( self ):
        return 0.5 * self.base * self.height

serialized_data = [
    {"_type": "Square", "side": 2.0},
    {"_type": "Triangle", "base": 1.75, "height": 2.50},
    {"_type": "Square", "side": 1.5},
]

for data in serialized_data:
    shape = objectfactory.Factory.create_object( data )
    print( 'class type: {}, shape area: {}'.format( type( shape ), shape.get_area() ) )

```
Output:
```
class type: <class '__main__.Square'>, shape area: 4.0
class type: <class '__main__.Triangle'>, shape area: 2.1875
class type: <class '__main__.Square'>, shape area: 2.25
```

See more examples [here](examples)

## Install
Use [pip](https://pip.pypa.io/en/stable/installing/) for installation
```
pip install objectfactory
```
