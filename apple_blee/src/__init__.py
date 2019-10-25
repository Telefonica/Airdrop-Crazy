from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import logging


# Creates the Flask application
app = Flask(__name__)
app.config.from_object('config')
application = app
socketio = SocketIO(app)
CORS(app)
jwt = JWTManager(app)

from src import views