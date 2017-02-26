from flask import (Flask, Blueprint, request, jsonify, 
    session as login_session, make_response)
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from app import DataManager, ccapp, utils

from oauth2client.client import FlowExchangeError

import httplib2, requests, traceback, json

api_bp = Blueprint('api', __name__)
Api(ccapp)
CORS(ccapp)


# data access endpoints

@ccapp.route('/user_type/', methods=['GET'])
def user_type_json():
    """JSON endpoint for serving user type data from the database.
    """
    #data = DataManager.getData()

    #return jsonify(Data=[i.serialize for i in data])


@ccapp.route('/user/id=<int:user_id>', methods=['GET'])
def user_json(user_id):
    """JSON endpoint for serving user data from the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)


@ccapp.route('/calorie/id=<int:calorie_id>+user_id=<int:calorie_id>+date_from=<int:date_from>+date_to=<int:date_to>+time_from=<int:time_from>+time_to=<int:time_time>/', 
        methods=['GET'])
def get_calorie(calorie_id, user_id, date_from, date_to, time_from, time_to):
    """Endpoint for serving calorie records from the database.

    Args:
        calorie_id: the id of the calorie to get
        user_id: the user id of the calorie's owner
        date_from: the beginning date of the range of calories to get
        date_to: the ending date of the range of calories to get
        time_from: the beginning time of the range of calories to get
        time_to: the ending time of the range of calories to get
    Return:
        A JSON representing the database version(s) of the calorie(s) specified
        by the given arguments
    """
    if len(calorie_id) > 1:
        calorie_id = int(calorie_id)
    else:
        calorie_id = None

    if len(user_id) > 1:
        user_id = int(user_id)
    else:
        user_id = None      

    if len(date_from) > 1:
        date_from = datetime.date(date_from)
    else:
        date_from = datetime.date.min

    if len(date_to) > 1:
        date_to = datetime.date(date_to)
    else:
        date_from = datetime.date.max

    if len(time_from) > 1:
        time_from = datetime.time(time_from)
    else:
        time_from = datetime.time.min

    if len(time_to) > 1:
        time_to = datetime.time(time_to)
    else:
        time_to = datetime.time.max

    calorie = DataManager.get_calorie(calorie_id=calorie_id, 
        user_id=user_id, date_from=date_from, date_to=date_to, 
        time_from=time_from, time_to=time_to)

    print calorie

    return jsonify(Data=calorie.serialize)

@ccapp.route('/calorie/id=<int:calorie_id>+user_id=<int:calorie_id>+date_from=<int:date_from>+date_to=<int:date_to>+time_from=<int:time_from>+time_to=<int:time_time>/', 
        methods=['GET'])
def edit_calorie(calorie_id, user_id, date_from, date_to, time_from, time_to):
    """Endpoint for editing calorie records in the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)

@ccapp.route('/calorie/user_id=<int:calorie_id>+date_from=<int:date_from>+date_to=<int:date_to>+time_from=<int:time_from>+time_to=<int:time_time>/', 
        methods=['GET'])
def create_calorie(user_id, date_from, date_to, time_from, time_to):
    """Endpoint for creating calorie records in the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)

# login/logout endpoints

@ccapp.route('/gconnect', methods=['POST'])
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
        oauth_flow = ccapp.config['G_OAUTH_FLOW']
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except:
        traceback.print_exc()
        response = make_response(json.\
            dumps('Failed to upgrade the authorization code.'), 401)
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
        response = make_response(json.\
            dumps("Token's user ID doesn't match given user"), 401)
        response.headers['Content-Type'] = 'application/json'

        return response
    
    # verify that the access token is valid for this app
    if result['issued_to'] != ccapp.config['G_CLIENT_ID']:
        response = make_response(json.\
            dumps("Token's client ID doesn't match app's ID"), 401)
        response.headers['Content-Type'] = 'application/json'

        return response
        
    # check to see if the google account is already logged into the system
    if ('gplus_id' in login_session and
        login_session['gplus_id'] == gplus_id):
        response = make_response(json.\
            dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'

        return response
    
    # store relevant credentials
    login_session['credentials'] = access_token
    login_session['gplus_id'] = gplus_id

    # get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['email'] = data['email']
    login_session['username'] = data['name']
    login_session['Access-Control-Allow-Origin'] = '*'

    utils.set_session_user_info()

    return jsonify({'username': login_session['username'],
                    'user_id': login_session['user_id'],
                    'user_type': login_session['user_type_id'],
                    'email': login_session['email'],
                    'exp_cal': login_session['exp_cal'],
                    'Access-Control-Allow-Origin': '*'})


@ccapp.route('/disconnect', methods=['POST'])
def disconnect():
    """Logout a user that is currently logged in.
    Returns immediately if no user is logged in.
    """
    if not utils.is_logged_in():

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


@ccapp.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    """Disconnect a user from Google OAuth.
    """
    access_token = login_session['credentials']
    
    # execute HTTP GET request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    discon_result = {'success':False,
                     'message':'Failed to disconnect from Google'}

    if result['status'] == '200':

        del login_session['gplus_id']
        discon_result['success'] = True
        discon_result['message'] = 'Disconnected from Google'

    return discon_result

'''
to incluce, possibly
def write_tables_to_json(path):
    """Write all of the tables in the database to .json files
    in the specified directory.
    """
    table_json_endpoints = [{'func':user_type_json, 'name':'UserType'},
                            {'func':user_json, 'name':'User'},
                            {'func':calorie_json, 'name':'Calorie'}]

    for table in table_json_endpoints:
        func = table['func']
        response = func()
        data = response.data
        name = func.__name__
        name = name[:-4]
        file = open(path+table['name']+'.json', 'w')
        file.write(data)
        file.close()
'''