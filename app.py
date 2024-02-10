from flask import Flask
from routes.routes import Routes
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
routes = Routes()
app.register_blueprint(routes.bp)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
