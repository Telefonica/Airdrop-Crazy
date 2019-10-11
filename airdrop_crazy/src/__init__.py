from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://d84d3d7d2ef948cbb41c6cea6e1acb2a@sentry.io/2040497",
    integrations=[FlaskIntegration()]
)

# Creates the Flask application
app = Flask(__name__)
app.config.from_object('config')
application = app
socketio = SocketIO(app)
CORS(app)
jwt = JWTManager(app)
# 6, 44, 149
IFACE="wlx503eaaec4c39"
CHANNEL="44"

from src import views