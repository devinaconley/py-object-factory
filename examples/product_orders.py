"""
product order example

use the objectfactory library to handle product orders across multiple vendors. validate incoming
order data, load as python objects, and calculate price and estimated delivery
"""

# src
import objectfactory


def main():
    raw_orders = [
        {
            '_type': 'DollarStoreProduct',
            'product_id': 'greeting_card',
            'quantity': 3
        },
        {
            '_type': 'EcommerceGiantProduct',
            'product_id': 'tv'
        },
        {
            '_type': 'EcommerceGiantProduct',
            'product_id': 'virtual_assistant',
            'quantity': 2
        }
    ]

    # deserialize raw product order
    products = [objectfactory.create_object( order, object_type=Product ) for order in raw_orders]

    # calculate overall price
    price = sum( [prod.get_price() * prod.quantity for prod in products] )
    print( 'Overall order price: ${}'.format( price ) )

    # estimate delivery
    days = max( [prod.get_delivery_time() for prod in products] )
    print( 'Estimated delivery time is: {} days'.format( days ) )

    # validate stocking
    in_stock = all( [prod.quantity < prod.get_quantity_in_stock() for prod in products] )
    print( 'Products are {}stocked'.format( '' if in_stock else 'not ' ) )


class Product( objectfactory.Serializable ):
    """
    base abstract class for our products
    """
    product_id = objectfactory.String()  # all products will have an id
    quantity = objectfactory.Integer( default=1 )  # all products will have a quantity

    def get_price( self ) -> float:
        """
        abstract method to calculate price and return

        :return: float
        """
        raise NotImplementedError( 'get_price method is required' )

    def get_delivery_time( self ) -> int:
        """
        abstract method to get required delivery time

        :return:
        """
        raise NotImplementedError( 'get_delivery_time method is required' )

    def get_quantity_in_stock( self ) -> int:
        """
        abstract method to get quantity in stock

        :return:
        """
        raise NotImplementedError( 'get_quantity_in_stock method is required' )


@objectfactory.register_class
class DollarStoreProduct( Product ):
    """
    product order from a dollar store vendor
    """

    def get_price( self ) -> float:
        """
        everything is a dollar!!!!

        :return:
        """
        return 1.00

    def get_delivery_time( self ) -> int:
        """
        everything takes about a week to ship

        :return:
        """
        return 7

    def get_quantity_in_stock( self ) -> int:
        """
        mock connection to this vendor's supply data

        :return:
        """
        return {
            'greeting_card': 300,
            'candle': 15,
            'glass_vase': 10
        }.get( self.product_id, 0 )


@objectfactory.register_class
class EcommerceGiantProduct( Product ):
    """
    product order from an e-commerce giant
    """

    def get_price( self ) -> float:
        """
        mock connection to this vendor's pricing data

        :return:
        """
        return {
            'really_inspiring_book': 15,
            'tv': 450,
            'digital_clock': 10,
            'virtual_assistant': 50
        }.get( self.product_id, None )

    def get_delivery_time( self ) -> int:
        """
        guaranteed 2-day delivery

        :return:
        """
        return 2

    def get_quantity_in_stock( self ) -> int:
        """
        infinite supplies

        :return:
        """
        return 1000000


if __name__ == '__main__':
    main()
