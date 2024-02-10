from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rental_management.Rental import Base, Rental


class RentalManager:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_rental(self, rental_name, rental_address, renter_name, rent_amount):
        with self.Session() as session:
            rental = Rental(rental_name, rental_address, renter_name, rent_amount)
            session.add(rental)
            session.commit()

    def list_rentals(self):
        with self.Session() as session:
            rentals = session.query(Rental).all()
            return rentals