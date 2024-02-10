from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user_management.User import Base, User
from MailJetClient import MailJetClient


class UserManager:
    def __init__(self, db_file, token_manager):
        self.engine = create_engine(f'sqlite:///{db_file}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.mailjet_client = MailJetClient()
        self.token_manager = token_manager

    def register_user(self, firstname, lastname, email, password):
        session = self.Session()

        # Check if the email is already taken
        existing_user = session.query(User).filter(User.email == email).first()
        if existing_user:
            session.close()
            return "You have an account with this email address. Please choose different email address to sign up."

        # Create a new user, send email for verification
        user = User(firstname, lastname, email, password)
        session.add(user)
        verification_token = self.token_manager.generate_verification_token(user)
        session.commit()
        session.close()

        verification_link = f"http://localhost:5000/verify_email?token={verification_token}"
        response_code = self.mailjet_client.send_email(email, firstname, verification_link)
        print(f"Email verification response code: {response_code}")

        return "Registration successful, please verify your email address to login!"

    def login(self, email, password):
        session = self.Session()
        user = session.query(User).filter(User.email == email).first()
        if user is not None:
            if user.verify_password(password):
                if user.is_verified:
                    session.close()
                    return { "status": 200, "message": "Login successful!" }
                else:
                    session.close()
                    return { "status": 401, "message": "Account not verified. Please check your email for verification instructions." }
            else:
                session.close()
                return { "status": 401, "message": "Invalid email address or password" }
        session.close()
        return { "status": 401, "message": "Invalid email address or password" }

    def set_verified(self, email):
        session = self.Session()
        user = session.query(User).filter(User.email == email).first()
        if user:
            user.set_verified()
            session.commit()
            session.close()
            return True
        session.close()
        return False