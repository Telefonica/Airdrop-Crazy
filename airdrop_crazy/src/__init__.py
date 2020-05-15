from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask.cli import with_appcontext
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from src.network_config import NetworkConfig

SENTRY_DNS=""

sentry_sdk.init(
    dsn=SENTRY_DNS,
    integrations=[FlaskIntegration()]
)

network_config = NetworkConfig()

# Creates the Flask application
app = Flask(__name__)
app.config.from_object('config')
application = app
socketio = SocketIO(app)
CORS(app)
jwt = JWTManager(app)


from src import views