import os
import logging

from flask import Blueprint, request, jsonify, session
from token_management.TokenManager import TokenManager
from user_management.UserManager import UserManager

DB_FILE = "user_database.db"
APP_SECRET_KEY = os.environ['APP_SECRET_KEY']


class UserRoutes:
    def __init__(self):
        self.bp = Blueprint("routes", __name__)
        self.register_routes()
        self.token_manager = TokenManager(APP_SECRET_KEY)
        self.user_manager = UserManager(DB_FILE, self.token_manager)

    def home(self):
        return "Welcome to the User Management Application!"

    def register_user(self):
        data = request.get_json()
        if data:
            firstname = data.get("firstname")
            lastname = data.get("lastname")
            email = data.get("email")
            password = data.get("password")
        response = self.user_manager.register_user(firstname, lastname, email, password)
        return jsonify({"message": response}), 201

    def login(self):
        data = request.get_json()
        if data:
            email = data.get("email")
            password = data.get("password")

        # TODO: remove testing code for session
        logging.info('email: %s, password: %s', email, password)
        if 'email' in session:
            return {'status': 200, 'message': 'Already logged in'}

        response = self.user_manager.login(email, password)
        if response['status'] == 200:
            session['email'] = email
        return jsonify(response), response['status']

    def logout(self):
        if 'email' in session:
            # del session['email']
            session.clear()
            return {'status': 200, 'message': 'Log out successful'}

        return {'status': 200, 'message': 'User already logged out'}

    def is_authorized(self):
        if 'email' in session:
            return {'isAuthorized': True}
        return {'isAuthorized': False}

    # Verify email route
    def verify_email(self):
        data = request.args
        token = data.get('token')
        email = self.token_manager.verify_token_and_get_email(token)
        if not email:
            return jsonify({'message': 'Invalid/expired verification token.'}), 401
        is_verified = self.user_manager.set_verified(email)
        if is_verified:
            return jsonify({'message': 'Account verified successfully.'}), 200
        else:
            return jsonify({'message': 'Invalid token or user not found.'}), 400

    def register_routes(self):
        self.bp.add_url_rule("/", "home", self.home)
        self.bp.add_url_rule("/signup", "register_user", self.register_user, methods=["POST"])
        self.bp.add_url_rule("/signin", "login", self.login, methods=["POST"])
        self.bp.add_url_rule('/verify_email', "verify_email", self.verify_email, methods=['GET'])
        self.bp.add_url_rule('/logout', "logout", self.logout, methods=['POST'])
        self.bp.add_url_rule('/isAuthorized', "is_authorized", self.is_authorized, methods=['GET'])