import hashlib

from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, primary_key=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = self._hash_password(password)
        self.is_verified = False

    def _hash_password(self, password):
        # Use a secure hashing algorithm like bcrypt or Argon2 in production
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        hashed_password = self._hash_password(password)
        return self.password == hashed_password

    def set_verified(self):
        self.is_verified = True