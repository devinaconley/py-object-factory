# py-object-factory

[![Build Status](https://app.travis-ci.com/devinaconley/py-object-factory.svg?branch=develop)](https://app.travis-ci.com/devinaconley/py-object-factory)
[![codecov](https://codecov.io/gh/devinaconley/py-object-factory/branch/develop/graph/badge.svg)](https://codecov.io/gh/devinaconley/py-object-factory)
[![Documentation Status](https://readthedocs.org/projects/objectfactory/badge/?version=latest)](https://objectfactory.readthedocs.io/en/latest/?badge=latest)


**objectfactory** is a python package to easily implement the factory design pattern for object creation, serialization, and polymorphism
- designed to support polymorphism
- integrates seamlessly with [marshmallow](https://github.com/marshmallow-code/marshmallow)
  and other serialization frameworks
- schema inherent in class definition
- load any object with a generic interface
- serialize objects to JSON

## Example 
Simple **shapes** example:
```python
import objectfactory

@objectfactory.register
class Square(objectfactory.Serializable):
    side = objectfactory.Field()

    def get_area(self):
        return self.side * self.side

@objectfactory.register
class Triangle(objectfactory.Serializable):
    base = objectfactory.Field()
    height = objectfactory.Field()

    def get_area(self):
        return 0.5 * self.base * self.height

serialized_data = [
    {"_type": "Square", "side": 2.0},
    {"_type": "Triangle", "base": 1.75, "height": 2.50},
    {"_type": "Square", "side": 1.5},
]

for data in serialized_data:
    shape = objectfactory.create(data)
    print('class type: {}, shape area: {}'.format(type(shape), shape.get_area()))
```

Output:
```
class type: <class '__main__.Square'>, shape area: 4.0
class type: <class '__main__.Triangle'>, shape area: 2.1875
class type: <class '__main__.Square'>, shape area: 2.25
```

### More examples
See more advanced examples [here](https://github.com/devinaconley/py-object-factory/tree/develop/examples)

## Install
Use [pip](https://pip.pypa.io/en/stable/installing/) for installation
```
pip install objectfactory
```

## Documentation
Read the full documentation at [objectfactory.readthedocs.io](https://objectfactory.readthedocs.io/)
