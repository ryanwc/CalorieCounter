from flask import (Blueprint, render_template, request, redirect, url_for, 
    flash, session as login_session, make_response)
from functools import wraps

from oauth2client.client import FlowExchangeError

import json, httplib2, requests, traceback, random, string

import app.DataManager, app
from app.utils import (get_client_login_session, set_session_user_info,
                       get_signin_alert, is_logged_in)


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


@app.route('/')
@app.route('/index/')
@app.route('/login/')
def calorie_counter_home():
    """Serve the Calorie Counter homepage
    """
    # create a state token to prevent CSRF
    # store it in the session for later validation
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.ascii_lowercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    client_login_session = get_client_login_session()

    # for writing all existing db data to .json
    #writeTablesToJSON('initial_data/')

    return render_template("index.html", state=state, 
                           client_login_session=client_login_session)


# Login/logout endpoints


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Ajax endpoint for google sign in authentication
    """
    # confirm entity with correct 3rd party credentials is same entity 
    # that is trying to login from the current login page's session.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 
            401)
        response.headers['Content-Type'] = 'application/json'

        return response

    code = request.data

    try:
        # upgrade the authorization code into a credentials object
        # i.e., give google the data (one time code) the entity to be 
        # authenticated supposedly got from google and have google 
        # return credentials if the data is correct
        oauth_flow = app.config['G_OAUTH_FLOW']
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except:
        traceback.print_exc()
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # check that the access token from google is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
       % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # if there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

        return response
    
    # verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user"), 401)
        response.headers['Content-Type'] = 'application/json'

        return response
    
    # verify that the access token is valid for this app
    if result['issued_to'] != app.config['G_CLIENT_ID']:
        response = make_response(json.dumps("Token's client ID doesn't match app's ID"), 401)
        response.headers['Content-Type'] = 'application/json'

        return response
        
    # check to see if the google account is already logged into the system
    if ('gplus_id' in login_session and
        login_session['gplus_id'] == gplus_id):
        response = make_response(json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'

        return response
    
    # store relevant credentials
    login_session['g_credentials'] = credentials
    login_session['credentials'] = {'access_token':access_token}
    login_session['gplus_id'] = gplus_id

    # get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['email'] = data['email']
    login_session['picture'] = data['picture']
    login_session['username'] = data['name']

    set_session_user_info()

    return get_signin_alert()


@app.route('/disconnect', methods=['POST'])
def disconnect():
    """Logout a user that is currently logged in.
    Returns immediately if no user is logged in.
    """
    if not is_logged_in():

        response = make_response(json.dumps('No user logged in'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    discon_result = None

    # login tied to google account, so this should always be true
    # TO-DO: make less brittle
    if 'gplus_id' in login_session:
        discon_result = gdisconnect()
    else:
        return "unknown error"

    logout_message = ""

    if discon_result is not None:
        if discon_result['success']:
            logout_message += discon_result['message']
            logout_message += ";  "
        else:
            response = make_response(json.dumps('Failed to revoke '+\
                'third party authorization'), 401)
            response.headers['Content-Type'] = 'application/json'

            return response

    username = login_session['username']

    del login_session['credentials']
    del login_session['user_id']
    del login_session['username']
    del login_session['email']

    logout_message += "Logged " + username + " out of Calorie Counter"

    return logout_message


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    """Disconnect a user from Google OAuth.
    """
    access_token = login_session['credentials']['access_token']
    
    # execute HTTP GET request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    discon_result = {'success':False,
                     'message':'Failed to disconnect from Google'}

    if result['status'] == '200':

        del login_session['g_credentials']
        del login_session['gplus_id']
        discon_result['success'] = True
        discon_result['message'] = 'Disconnected from Google'

    return discon_result
