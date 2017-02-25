from flask import Flask, session as login_session

ccapp = Flask(__name__, instance_relative_config=True)

ccapp.config.from_object('config')
ccapp.config.from_pyfile('config.py')

from .home.home import home_bp
from .api.api import api_bp

ccapp.register_blueprint(home_bp, url_prefix='/home')
ccapp.register_blueprint(api_bp, url_prefix='/api')
