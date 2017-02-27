from flask import (Flask, Blueprint, request, jsonify, 
    session as login_session, make_response)
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from app import DataManager, ccapp, utils

from oauth2client.client import FlowExchangeError

import httplib2, requests, traceback, json, datetime

api_bp = Blueprint('api', __name__)
Api(ccapp)
CORS(ccapp)


# data access endpoints

@ccapp.route('/user_type', methods=['GET', 'POST'])
def user_type():
    """Endpoint for serving user type records from the database.

    Args that can be sent as part of http query string:
        user_type_id: A user type id
        name: A user type name
        CRUD_self: whether the user type(s) to get can edit its own
        calorie entries
        CRUD_users: whether the user type(s) to get can edit other
        users (but not their calorie entries)
        CRUD_all: whether the user type to get can edit all users and
        calorie entries
    Return:
        A JSON representing the database version(s) of the user type(s) 
        specified by the given arguments
    """
    if request.args.get("user_type_id") and \
        len(request.args.get("user_type_id")) > 0:
        user_type_id = int(request.args.get("user_type_id"))
    else:
        user_type_id = None

    if request.args.get("name") and \
        len(request.args.get("name")) > 0:
        name = int(request.args.get("name"))
    else:
        name = None    

    if request.args.get("CRUD_self") and \
        len(request.args.get("CRUD_self")) > 0:
        CRUD_self = request.args.get("CRUD_self")
    else:
        CRUD_self = None

    if request.args.get("CRUD_users") and \
        len(request.args.get("CRUD_users")) > 0:
        CRUD_users = request.args.get("CRUD_users")
    else:
        CRUD_users = None

    if request.args.get("CRUD_all") and \
        len(request.args.get("CRUD_all")) > 0:
        CRUD_all = request.args.get("CRUD_all")
    else:
        CRUD_all = None

    user_type = DataManager.get_user_type(user_type_id=user_type_id, name=name, 
        CRUD_self=CRUD_self, CRUD_users=CRUD_users, CRUD_all=CRUD_all)

    if id in user_type:
        # single result
        return jsonify(Data=[user_type.serialize])
    elif len(user_type) > 0:
        # multiple results
        return jsonify(Data=[i.serialize for i in user_type])
    else:
        # no results, return empty list
        return jsonify(user_type)


@ccapp.route('/delete_user_type', methods=['POST'])
def delete_user_type():
    """Endpoint for deleting user type records from the database.

    Args that can be sent as part of http query string:
        user_type_id: the id of the user type to delete
    Return:
        A JSON representing deletion success or failure
    """
    if request.args.get("user_type_id") and \
        len(request.args.get("user_type_id")) > 0:

        user_type_id = int(request.args.get("user_type_id"))
        DataManager.delete_user(user_type_id)
        return jsonify({"Message": "Deleted calorie " + user_type_id})
    else:

        response = make_response(json.dumps('Invalid user type id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/user', methods=['GET', 'POST'])
def user():
    """Endpoint for serving user records from the database.

    Args that can be sent as part of http query string:
        user_id: the id of the user to get
        email: the email of the user to get
        username: the username of the user to get
    Return:
        A JSON representing the database version(s) of the user(s) specified
        by the given arguments
    """
    print request.args

    if request.args.get("user_id") and \
        len(request.args.get("user_id")) > 0:
        user_id = int(request.args.get("user_id"))
    else:
        user_id = None

    if request.args.get("username") and \
        len(request.args.get("username")) > 0:
        username = int(request.args.get("username"))
    else:
        username = None    

    if request.args.get("email") and \
        len(request.args.get("email")) > 0:
        email = request.args.get("email")
    else:
        email = None

    user = DataManager.get_user(user_id=user_id, username=username, email=email)

    if id in user:
        # single result
        return jsonify(Data=[user.serialize])
    elif len(user) > 0:
        # multiple results
        return jsonify(Data=[i.serialize for i in user])
    else:
        # no results, return empty list
        return jsonify(user)


@ccapp.route('/delete_user', methods=['POST'])
def delete_user():
    """Endpoint for deleting user records from the database.

    Args that can be sent as part of http query string:
        user_id: the id of the user to delete
    Return:
        A JSON representing deletion success or failure
    """
    if request.args.get("user_id") and \
        len(request.args.get("user_id")) > 0:

        user_id = int(request.args.get("user_id"))
        DataManager.delete_user(user_id)
        return jsonify({"Message": "Deleted calorie " + user_id})
    else:

        response = make_response(json.dumps('Invalid user id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/calorie', methods=['GET'])
def get_calorie():
    """Endpoint for serving calorie records from the database.

    Args that can be sent as part of http query string:
        calorie_id: the id of the calorie to get
        user_id: the user id of the calorie's owner
        date_from: the beginning date of the range of calories to get.
            must be given in 'YYYY-MM-DD' format
        date_to: the ending date of the range of calories to get.
            must be given in 'YYYY-MM-DD' format
        time_from: the beginning time of the range of calories to get.
            must be given as an hour, from 0 <= h <= 24
        time_to: the ending time of the range of calories to get
            must be given as an hour, from 0 <= h <= 24
    Return:
        A JSON representing the database version(s) of the calorie(s) specified
        by the given arguments
    """
    if request.args.get("calorie_id") and \
        len(request.args.get("calorie_id")) > 0:
        calorie_id = int(request.args.get("calorie_id"))
    else:
        calorie_id = None

    if request.args.get("user_id") and \
        len(request.args.get("user_id")) > 0:
        user_id = int(request.args.get("user_id"))
    else:
        user_id = None    

    if request.args.get("date_from") and \
        len(request.args.get("date_from")) > 0:
        dates = request.args.get("date_from").split("-")
        date_from = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
    else:
        date_from = datetime.date.min

    if request.args.get("date_to") and \
        len(request.args.get("date_to")) > 0:
        dates = request.args.get("date_to").split("-")
        date_to = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
    else:
        date_to = datetime.date.max

    if request.args.get("time_from") and \
        len(request.args.get("time_from")) > 0:
        time_from = datetime.time(int(request.args.get("time_from")))
    else:
        time_from = datetime.time.min

    if request.args.get("time_to") and \
        len(request.args.get("time_to")) > 0:
        time_to = datetime.time(int(request.args.get("time_to")))
    else:
        time_to = datetime.time.max

    calorie = DataManager.get_calorie(calorie_id=calorie_id, 
        user_id=user_id, date_from=date_from, date_to=date_to, 
        time_from=time_from, time_to=time_to)

    # if results, set daytotal and whether the calorie falls on passing day
    if id in calorie:
        # single result
        (daytotal, meets) = utils.pass_fail_cal(calorie)
        sCal = calorie.serialize
        sCal["daytotal"] = daytotal
        sCal["meets"] = meets
        utils.pass_fail_cal(calorie)
        return jsonify(Data=[sCal])
    elif len(calorie) > 0:
        # multiple results
        sCals = []
        for cal in calorie:
            (daytotal, meets) = utils.pass_fail_cal(cal)
            sCal = cal.serialize
            sCal["daytotal"] = daytotal
            sCal["meets"] = meets
            sCals.append(sCal)
        return jsonify(Data=sCals)
    else:
        # no results, return empty list
        return jsonify(calorie)

@ccapp.route('/add_calorie', methods=['POST'])
def add_calorie():
    """Endpoint for adding calorie records in the database.

    Args that can be sent as part of http query string:
        user_id: the calorie's user id
        date: the calorie's date. must be given in 'YYYY-MM-DD' format
        time: the calorie's time. must be given as an hour, from 0 <= h <= 24
        text: the calorie's description
        amnt: the new number of calories
    Return:
        A JSON representing the database version(s) of the created calorie
    """
    print request.args

    if request.args.get("user_id") and \
        len(request.args.get("user_id")) > 0:
        user_id = int(request.args.get("user_id"))
    else:
        response = make_response(json.dumps('Must provide valid user id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.args.get("date") and \
        len(request.args.get("date")) > 0:
        dates = request.args.get("date").split("-")
        date = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
    else:
        response = make_response(json.dumps('Must provide valid date'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.args.get("time") and \
        len(request.args.get("time")) > 0:
        time = datetime.time(int(request.args.get("time")))
    else:
        response = make_response(json.dumps('Must provide valid time'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.args.get("text") and \
        len(request.args.get("text")) > 0:
        text = request.args.get("text")
    else:
        response = make_response(json.dumps('Must provide valid text'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.args.get("amnt") and \
        len(request.args.get("amnt")) > 0:
        amnt = request.args.get("amnt")
    else:
        response = make_response(json.dumps('Must provide valid amount'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    cal_id = DataManager.add_calorie(user_id, date, time, text, amnt)
    calorie = DataManager.get_calorie(calorie_id=cal_id)

    if calorie:
        return jsonify(Data=[calorie.serialize])
    else:
        response = make_response(json.dumps('Internal server error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/edit_calorie', methods=['POST'])
def edit_calorie():
    """Endpoint for editing calorie records in the database.

    Args that can be sent as part of http query string:
        calorie_id: the id of the calorie to edit
        user_id: the new user id
        date: the new date. must be given in 'YYYY-MM-DD' format
        time: the new time. must be given as an hour, from 0 <= h <= 24
        text: the new description
        num_calories: the new number of calories
    Return:
        A JSON representing the database version of the updated calorie
    """
    if request.args.get("calorie_id") and \
        len(request.args.get("calorie_id")) > 0:
        calorie_id = int(request.args.get("calorie_id"))
    else:
        response = make_response(json.dumps('Must provide calorie id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.args.get("user_id") and \
        len(request.args.get("user_id")) > 0:
        user_id = int(request.args.get("user_id"))
    else:
        user_id = None

    if request.args.get("date") and \
        len(request.args.get("date")) > 0:
        dates = request.args.get("date").split("-")
        date = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
    else:
        date = None

    if request.args.get("time") and \
        len(request.args.get("time")) > 0:
        time = datetime.time(int(request.args.get("time")))
    else:
        time = None

    if request.args.get("text") and \
        len(request.args.get("text")) > 0:
        text = request.args.get("text")
    else:
        text = None

    if request.args.get("amnt") and \
        len(request.args.get("amnt")) > 0:
        amnt = request.args.get("amnt")
    else:
        amnt = None 

    DataManager.edit_calorie(calorie_id, user_id=user_id, date=date,
        time=time, text=text, num_calories=amnt)
    calorie = DataManager.get_calorie(calorie_id=calorie_id)

    print calorie

    if calorie:
        return jsonify(Data=[calorie.serialize])
    else:
        response = make_response(json.dumps('Internal server error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/delete_calorie', methods=['POST'])
def delete_calorie():
    """Endpoint for deleting calorie records from the database.

    Args that can be sent as part of http query string:
        calorie_id: the id of the calorie to delete
    Return:
        A JSON representing deletion success or failure
    """
    if request.args.get("calorie_id") and \
        len(request.args.get("calorie_id")) > 0:

        calorie_id = int(request.args.get("calorie_id"))
        result = DataManager.delete_calorie(calorie_id)
        if result == 1:
            return jsonify({"Message": "Successful deletion",
                            "Post": "deletion",
                            "Model": "calorie",
                            "Id": calorie_id})
        else:
            response = make_response(json.\
                dumps('Calorie id did not match any in db'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        response = make_response(json.dumps('Invalid calorie id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

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
        # if so just return their credentials

        return jsonify({'username': login_session['username'],
                    'user_id': login_session['user_id'],
                    'user_type': login_session['user_type_id'],
                    'email': login_session['email'],
                    'exp_cal': login_session['exp_cal'],
                    'Access-Control-Allow-Origin': '*'})
    
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

    return jsonify(discon_result)
