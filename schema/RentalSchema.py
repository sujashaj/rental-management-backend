from schema.schema import ma
from rental_management.Rental import Rental

class RentalSchema(ma.Schema):
    class Meta:
        model = Rental
        load_instance = True
        fields = ('rental_name','rental_address','renter_name','rent_amount')

rental_schema = RentalSchema()
rentals_schema = RentalSchema(many=True)
