from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user_management.User import Base, User


class UserManager:
    def __init__(self, db_file):
            self.engine = create_engine(f'sqlite:///{db_file}')
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind = self.engine)

    def register_user(self, username, email, password):
            session = self.Session()

            existing_user = session.query(User).filter(User.username == username or User.email == email).first()
            if existing_user:
                session.close()
                return "Username or email is already taken.Please choose different credentials"

            user = User(username, email, password)
            session.add(user)
            session.commit()
            session.close()
            return "Registration successful!"

    def login(self, username, password):
            session = self.Session()
            user = session.query(User).filter(User.username == username).first()
            if user is not None:
                if user.verify_password(password):
                    if user.is_verified:
                         session.close()
                         return "Login successful!"
                    else:
                        session.close()
                        return "Account not verified. Please check your email for verification instructions."
                else:
                    session.close()
                    return "Incorrect password"
            session.close()
            return "User not found."










