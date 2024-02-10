from mailjet_rest import Client
import os

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
SENDER_EMAIL = os.environ['SENDER_EMAIL']
SENDER_NAME = os.environ['SENDER_NAME']


class MailJetClient:
    def __init__(self):
        self.mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

    def send_email(self, receiver_email, receiver_name, verification_link):
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "{}".format(SENDER_EMAIL),
                        "Name": "{}".format(SENDER_NAME)
                    },
                    "To": [
                        {
                            "Email": "{}".format(receiver_email),
                            "Name": "{}".format(receiver_name)
                        }
                    ],
                    "Subject": "Please verify your email address!",
                    "TextPart": "Greetings from user management application!",
                    "HTMLPart": f"May the delivery force be with you! Please click on this url to verify"
                                "your email address: {}".format(verification_link)
                }
            ]
        }
        result = self.mailjet.send.create(data=data)
        return result.status_code



