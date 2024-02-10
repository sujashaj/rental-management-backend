from dataclasses import dataclass
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


@dataclass
class Rental(Base):
    __tablename__ = 'Rental'

    rental_name = Column(String, primary_key=True)
    rental_address = Column(String, primary_key=True)
    renter_name = Column(String, primary_key=True)
    rent_amount = Column(Integer)

    def __init__(self, rental_name, rental_address, renter_name, rent_amount):
        self.rental_name = rental_name
        self.rental_address = rental_address
        self.renter_name = renter_name
        self.rent_amount = rent_amount