import jwt
from datetime import datetime, timedelta


class TokenManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_verification_token(self, user):
        payload = {
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=1)  # Access token expiration time
        }
        verification_token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return verification_token

    def verify_token_and_get_email(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if type(payload) == dict and payload.get('email') and payload.get('exp'):
                return payload.get('email')
            return None

        except jwt.DecodeError:
            return None
        except jwt.ExpiredSignatureError:
            return None