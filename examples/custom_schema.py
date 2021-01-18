"""
custom marshmallow schema example

use the objectfactory library with a custom marshmallow schema
to validate and load contact information
"""
import objectfactory
import marshmallow


def main():
    contacts = [
        {
            '_type': 'Contact',
            'first_name': 'john',
            'last_name': 'smith',
            'phone_number': '123-456-7890',
            'email': 'johnsmith@gmail.com'
        },
        {
            '_type': 'Contact',
            'first_name': 'john',
            'last_name': 'smith',
            'phone_number': '123-456-78',
            'email': 'johnsmith@gmail.com'
        },
        {
            '_type': 'Contact',
            'first_name': 'john',
            'last_name': 'smith',
            'phone_number': '123-456-7890',
            'email': 'nonsense'
        }
    ]

    # load and validate each contact
    for c in contacts:
        try:
            contact = objectfactory.create( c, object_type=Contact )
            print(
                'Loaded contact for: {} {}, number: {}, email: {}'.format(
                    contact.first_name,
                    contact.last_name,
                    contact.phone_number,
                    contact.email
                )
            )
        except marshmallow.ValidationError as e:
            print( 'Validation error: {}'.format( e ) )


class PhoneNumber( marshmallow.fields.Field ):
    """Custom marshmallow field to validate phone number"""

    def _deserialize( self, value, *args, **kwargs ):
        try:
            x = value.split( '-' )
            assert len( x ) == 3
            assert len( x[0] ) == 3
            assert len( x[1] ) == 3
            assert len( x[2] ) == 4
            return str( value )

        except AssertionError as e:
            raise marshmallow.ValidationError( 'Invalid phone number' )

    def _serialize( self, value, *args, **kwargs ):
        return str( value )


class ContactSchema( marshmallow.Schema ):
    """Custom marshmallow schema for contact info"""

    first_name = marshmallow.fields.Str()
    last_name = marshmallow.fields.Str()
    email = marshmallow.fields.Email()
    phone_number = PhoneNumber()


@objectfactory.register
class Contact( objectfactory.Serializable, schema=ContactSchema ):
    """
    product order from a dollar store vendor
    """
    first_name = objectfactory.String()
    last_name = objectfactory.String()
    email = objectfactory.String()
    phone_number = objectfactory.String()


if __name__ == '__main__':
    main()
