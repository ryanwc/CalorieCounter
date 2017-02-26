from flask import (Blueprint, render_template, request, redirect, url_for, 
    flash, session as login_session)
from functools import wraps

import json, random, string

from app import DataManager, ccapp
from app import utils


home_bp = Blueprint('home', __name__, 
    template_folder='templates', static_folder='static')


# Custom permissions decorators

def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash("You must be logged in to view that page")
            return redirect(url_for('calorie_counter_home'))
        return function(*args, **kwargs)
    return decorated_function


# Homepage view

@ccapp.route('/')
@ccapp.route('/index/')
@ccapp.route('/login/')
@ccapp.route('/home/')
def calorie_counter_home():
    """Serve the Calorie Counter homepage
    """
    # create a state token to prevent CSRF
    # store it in the session for later validation
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.ascii_lowercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    client_login_session = utils.get_client_login_session()

    # for writing all existing db data to .json
    #writeTablesToJSON('initial_data/')

    return render_template("home.html", state=state, 
                           client_login_session=client_login_session)
