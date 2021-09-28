"""
shapes example

use the objectfactory library to load shapes of various object types and
calculate their area accordingly
"""
import objectfactory


def main():
    serialized_data = [
        {"_type": "Square", "side": 2.0},
        {"_type": "Triangle", "base": 1.75, "height": 2.50},
        {"_type": "Square", "side": 1.5},
    ]

    # load each shape, printing object type and area
    for data in serialized_data:
        shape = objectfactory.create( data )
        print( 'class type: {}, shape area: {}'.format( type( shape ), shape.get_area() ) )


@objectfactory.register
class Square( objectfactory.Serializable ):
    """
    serializable square class
    """
    side = objectfactory.Float()

    def get_area( self ) -> float:
        """
        calculate area of square

        :return: side^2
        """
        return self.side * self.side


@objectfactory.register
class Triangle( objectfactory.Serializable ):
    """
    serializable triangle class
    """
    base = objectfactory.Float()
    height = objectfactory.Float()

    def get_area( self ) -> float:
        """
        calculate area of triangle

        :return: 0.5 * base * height
        """
        return 0.5 * self.base * self.height


if __name__ == '__main__':
    main()
