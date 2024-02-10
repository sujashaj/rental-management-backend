import os

from flask import Blueprint, request, jsonify
from token_management.TokenManager import TokenManager
from user_management.UserManager import UserManager

DB_FILE = "user_database.db"
APP_SECRET_KEY = os.environ['APP_SECRET_KEY']


class Routes:
    def __init__(self):
        self.bp = Blueprint("routes", __name__)
        self.register_routes()
        self.token_manager = TokenManager(APP_SECRET_KEY)
        self.user_manager = UserManager(DB_FILE, self.token_manager)


    def home(self):
        return "Welcome to the User Management Application"

    def register_user(self):
        data = request.get_json()
        if data:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
        response = self.user_manager.register_user(username, email, password)
        return jsonify({"message": response}), 201

    def login(self):
        data = request.get_json()
        if data:
            username = data.get("username")
            password = data.get("password")
        response = self.user_manager.login(username, password)
        return jsonify({"message": response}), 200

    def verify_email(self):
        data = request.args
        token = data.get('token')
        username = self.token_manager.verify_token_and_get_username(token)
        if not username:
            return jsonify({'message': 'Invalid/expired verification token.'}), 401
        is_verified = self.user_manager.set_verified(username)
        if is_verified:
            return jsonify({'message': 'Account verified succesfully.'}), 200
        else:
            return jsonify({'message': 'Invalid token or user not found.'}), 400

    def register_routes(self):
        self.bp.add_url_rule("/", "home", self.home)
        self.bp.add_url_rule("/register_user", "register_user", self.register_user, methods=["POST"])
        self.bp.add_url_rule("/login", "login", self.login, methods=["POST"])
        self.bp.add_url_rule('/verify_email', "verify_email", self.verify_email, methods=['GET'])




