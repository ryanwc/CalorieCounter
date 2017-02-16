from flask import Flask, session as login_session
from .home.home import home_bp

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')

app.register_blueprint(home_bp, url_prefix='/home')
