from flask import Flask
from flask_session import Session
from flask_cors import CORS
from routes.UserRoutes import UserRoutes
from routes.RentalRoutes import RentalRoutes
from schema.schema import ma

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
ma.init_app(app)

user_routes = UserRoutes()
rental_routes = RentalRoutes()
app.register_blueprint(user_routes.bp)
app.register_blueprint(rental_routes.bp)

if __name__ == "__main__":
    app.run(debug=True)
