from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    dsn="https://dac5c93735864365b79630c1995dfbea@sentry.io/2031635",
    integrations=[FlaskIntegration()]
)


# Creates the Flask application, called in bootstrap.sh
app = Flask(__name__)
app.config.from_object('config')
application = app
CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)


from src import views