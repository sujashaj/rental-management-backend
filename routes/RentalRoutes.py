import os

from rental_management.RentalManager import RentalManager
from flask import Blueprint, request, jsonify, session
from schema.RentalSchema import rental_schema, rentals_schema

DB_FILE = "user_database.db"
APP_SECRET_KEY = os.environ['APP_SECRET_KEY']

class RentalRoutes:
    def __init__(self):
        self.bp = Blueprint("rental_routes", __name__)
        self.register_routes()
        self.rental_manager = RentalManager(DB_FILE)

    def add_rental(self):
        if 'email' not in session:
            return {'status': 401, 'message': 'Unauthorized'}, 401
        data = request.get_json()
        if data:
            rental_name = data.get("rental_name")
            rental_address = data.get("rental_address")
            renter_name = data.get("renter_name")
            rent_amount = data.get("rent_amount")
        try:
            self.rental_manager.add_rental(rental_name, rental_address, renter_name, rent_amount)
        except Exception:
            return jsonify({'message': 'Duplicate rental!'}), 400
        return jsonify({'message': 'Success'}), 201

    def list_rental(self):
        if 'email' not in session:
            return {'status': 401, 'message': 'Unauthorized'}, 401
        rentals = self.rental_manager.list_rentals()
        return rentals_schema.jsonify(rentals), 200

    def register_routes(self):
        self.bp.add_url_rule("/addRental", "add_rental", self.add_rental, methods=["POST"])
        self.bp.add_url_rule("/listRentals", "list_rental", self.list_rental, methods=["GET"])