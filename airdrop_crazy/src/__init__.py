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

SENTRY_DNS=""

sentry_sdk.init(
    dsn=SENTRY_DNS,
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
IFACE=""
CHANNEL="6"

from src import views