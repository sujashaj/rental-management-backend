from flask import Flask
from routes.routes import Routes
from flask_cors import CORS
from flask_session import Session


app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
routes = Routes()
app.register_blueprint(routes.bp)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
