from flask import (Flask, Blueprint, request, jsonify, 
    session as login_session, make_response)
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from app import DataManager, ccapp, utils

import oauth2client.client

import httplib2, requests, traceback, json, datetime, bleach

api_bp = Blueprint('api', __name__)
Api(ccapp)
CORS(ccapp)


# data access endpoints

@ccapp.route('/user_type', methods=['GET'])
def get_user_type():
    """Endpoint for serving user type records from the database.

    Args can be sent as key/value pairs in the query string ('GET').
    Args:
        None. This endpoint method will simply show which user types
        exist (and their properties)
    Return:
        A JSON representing the database version(s) of the user type(s) 
        specified by the given arguments
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    user_type = DataManager.get_user_type()

    if len(user_type) > 0:
        return jsonify(Data=[i.serialize for i in user_type])
    else:
        # no results, return empty list
        return jsonify(Data=[])


@ccapp.route('/add_user_type', methods=['GET', 'POST'])
def add_user_type():
    """Endpoint for adding user type records from the database.
    Currently unimplemented and unneeded. If user types need to be
    created, updated, or deleted, the super user should change from direct 
    connection to database.
    """


@ccapp.route('/edit_user_type', methods=['GET', 'POST'])
def edit_user_type():
    """Endpoint for editing user type records from the database.
    Currently unimplemented and unneeded. If user types need to be
    created, updated, or deleted, the super user should change from direct 
    connection to database.
    """

@ccapp.route('/delete_user_type', methods=['GET', 'POST'])
def delete_user_type():
    """Endpoint for deleting user type records from the database.
    Currently unimplemented and unneeded. If user types need to be
    created, updated, or deleted, the super user should change from direct 
    connection to database.
    """

@ccapp.route('/user', methods=['GET'])
def get_user():
    """Endpoint for serving user records from the database.

    Args can be sent as key/value pairs in the query string ('GET')
    Args are optional unless noted.
    Args:
        user_id: the id of the user to get
        email: the email of the user to get
        username: the username of the user to get
    Return:
        A JSON representing the database version(s) of the user(s) specified
        by the given arguments
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("user_id") and \
        len(request.values.get("user_id")) > 0:
        user_id = int(request.values.get("user_id"))
    else:
        user_id = None

    if request.values.get("username") and \
        len(request.values.get("username")) > 0:
        username = request.values.get("username")
    else:
        username = None

    if request.values.get("email") and \
        len(request.values.get("email")) > 0:
        email = request.values.get("email")
    else:
        email = None

    # check permissions
    if not utils.canUserCRUD(user_id, 
            login_session["user_id"], login_session["user_type_id"]):
        response = make_response(json.\
            dumps('Not authorized to get other user data'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    user = DataManager.get_user(user_id=user_id, username=username, email=email)

    if not type(user) is list:
        # single result
        return jsonify(Data=[user.serialize])
    elif len(user) > 0:
        # multiple results
        return jsonify(Data=[i.serialize for i in user])
    else:
        # no results, return empty list
        return jsonify(Data=[])


@ccapp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Endpoint for adding user records to the database.

    Args can be sent as key/value pairs in the query string ('GET'), or as
    key/value pairs in the content ('POST').
    Args are optional unless noted.
    Args:
        email: the email of the user (required)
        username: the username of the user (required)
        user_type_id: the type of user to add
        exp_cal_day: the expected calories / day of the user
    Return:
        A JSON representing the database version(s) of the user(s) specified
        by the given arguments
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 400)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("username") and \
        len(request.values.get("username")) > 0:
        username = bleach.clean(request.values.get("username"))
        if not utils.is_username(username):
            response = make_response(json.\
                dumps('username invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        username = None

    if request.values.get("email") and \
        len(request.values.get("email")) > 0:
        email = bleach.clean(request.values.get("email"))
        if not utils.is_email(email):
            response = make_response(json.\
                dumps('email invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        email = None

    if request.values.get("exp_cal_day") and \
        len(request.values.get("exp_cal_day")) > 0:
        exp_cal_day = int(bleach.clean(request.values.get("exp_cal_day")))
        if not utils.is_exp_cal(exp_cal_day):
            response = make_response(json.\
                dumps('exp_cal_day invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        exp_cal_day = None 

    if request.values.get("user_type_id") and \
        len(request.values.get("user_type_id")) > 0:
        user_type_id = int(bleach.clean(request.values.get("user_type_id")))
        if not utils.is_user_type_id(user_type_id):
            response = make_response(json.\
                dumps('user_type_id invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        user_type_id = None   

    # check permissions
    if not utils.canUserCRUD(None, 
            login_session["user_id"], login_session["user_type_id"]):
        response = make_response(json.\
            dumps('Not authorized to get other user data'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    if user_type_id and not utils.canSetPermissions(login_session["user_type_id"]):
        response = make_response(json.\
            dumps('Not authorized to set user perissions'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    user_id = DataManager.add_user(username, email, 
        exp_cal_day=exp_cal_day, user_type_id=user_type_id)
    user = DataManager.get_user(user_id=user_id)

    if user:
        return jsonify(Data=[user.serialize])
    else:
        response = make_response(json.dumps('User creation error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    """Endpoint for editing user records in the database.

    Args can be sent as key/value pairs in the query string ('GET'), or as
    key/value pairs in the content ('POST').
    Args are optional unless noted.
    Args:
        user_id: the id of the user to edit REQUIRED
        email: the new email
        username: the new username
        exp_cal_day the new expected calories / day
        user_type_id: the id of the new user type
    Return:
        A JSON representing the given user edited as specified
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("user_id") and \
        len(request.values.get("user_id")) > 0:
        user_id = int(bleach.clean(request.values.get("user_id")))
    else:
        response = make_response(json.dumps('Must provide user id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.values.get("username") and \
        len(request.values.get("username")) > 0:
        username = bleach.clean(request.values.get("username"))
        if not utils.is_username(username):
            response = make_response(json.\
                dumps('username invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        username = None    

    if request.values.get("email") and \
        len(request.values.get("email")) > 0:
        email = bleach.clean(request.values.get("email"))
        if not utils.is_email(email):
            response = make_response(json.\
                dumps('email invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        email = None

    if request.values.get("exp_cal_day") and \
        len(request.values.get("exp_cal_day")) > 0:
        exp_cal_day = int(bleach.clean(request.values.get("exp_cal_day")))
        if not utils.is_exp_cal(exp_cal_day):
            response = make_response(json.\
                dumps('exp_cal_day invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        exp_cal_day = None

    if request.values.get("user_type_id") and \
        len(request.values.get("user_type_id")) > 0:
        user_type_id = int(bleach.clean(request.values.get("user_type_id")))
        if not utils.is_user_type_id(user_type_id):
            response = make_response(json.\
                dumps('user_type_id invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        user_type_id = None     

    userCheck = DataManager.get_user(user_id=user_id)

    # check permissions
    # if the logged in user can't do user actions
    if not utils.canUserCRUD(userCheck.id, 
            login_session["user_id"], login_session["user_type_id"]):
        response = make_response(json.\
            dumps('Not authorized for actions on given user'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    # if the logged in user is trying to set user permissions and can't
    if user_type_id and not utils.canSetPermissions(login_session["user_type_id"]):
        response = make_response(json.\
            dumps('Not authorized to set user permissions'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    DataManager.edit_user(user_id=user_id, username=username, email=email, 
        exp_cal_day=exp_cal_day, user_type_id=user_type_id)

    user = DataManager.get_user(user_id=user_id)

    if user:
        return jsonify(Data=[user.serialize])
    else:
        response = make_response(json.dumps('Internal server error on update'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

@ccapp.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    """Endpoint for deleting user records from the database.

    Args can be sent as key/value pairs in the query string ('GET'), or as
    key/value pairs in the content ('POST').
    Args:
        user_id: the id of the user to delete (REQUIRED)
    Return:
        A JSON representing deletion success or failure
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("user_id") and \
        len(request.values.get("user_id")) > 0:

        user_id = int(request.values.get("user_id"))
        user = DataManager.get_user(user_id=user_id)

        # check permissions
        if not utils.canUserCRUD(user.id, 
            login_session["user_id"], login_session["user_type_id"]):

            response = make_response(json.\
                dumps('Not authorized for actions on given user'), 403)
            response.headers['Content-Type'] = 'application/json'
            return response

        # if the user to be deleted can crud all, but login user can't
        login_crud_all = DataManager.\
            get_user_type(user_type_id=login_session["user_type_id"]).CRUD_all
        delete_crud_all = DataManager.\
            get_user_type(user_type_id=user.user_type_id).CRUD_all

        if delete_crud_all and not login_crud_all:
            response = make_response(json.\
                dumps('Not authorized to delete this user'), 403)
            response.headers['Content-Type'] = 'application/json'
            return response

        # update and return
        result = DataManager.delete_user(user_id)
        if result == 1:
            return jsonify({"Message": "Successful deletion",
                            "Post": "deletion",
                            "Model": "user",
                            "id": user_id})
        else:
            response = make_response(json.\
                dumps('User id did not match any in db'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        response = make_response(json.dumps('Invalid user id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/calorie', methods=['GET'])
def get_calorie():
    """Endpoint for serving calorie records from the database.

    Args can be sent as key/value pairs in the query string ('GET').
    All args are optional. Providing no args returns all calories.
    Args:
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
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("calorie_id") and \
        len(request.values.get("calorie_id")) > 0:
        calorie_id = int(bleach.clean(request.values.get("calorie_id")))
        # check permissions for reading this calorie
        calorie = DataManager.get_calorie(calorie_id=calorie_id)
        if not utils.canCalorieCRUD(calorie.user_id, 
                login_session["user_id"], login_session["user_type_id"]):
            response = make_response(json.\
                dumps('Not authorized for cal actions for given user'), 403)
            response.headers['Content-Type'] = 'application/json'
            return response 
    else:
        calorie_id = None

    if request.values.get("user_id") and \
        len(request.values.get("user_id")) > 0:
        user_id = int(bleach.clean(request.values.get("user_id")))
        # check perissions for reading this user's calories
        if not utils.canCalorieCRUD(user_id, 
                login_session["user_id"], login_session["user_type_id"]):
            response = make_response(json.\
            dumps('Not authorized for cal actions for given user'), 403)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        user_id = None    

    if request.values.get("date_from") and \
        len(request.values.get("date_from")) > 0:
        dates = request.values.get(bleach.clean("date_from")).split("-")
        date_from = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
    else:
        date_from = datetime.date.min

    if request.values.get("date_to") and \
        len(request.values.get("date_to")) > 0:
        dates = request.values.get(bleach.clean("date_to")).split("-")
        date_to = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
    else:
        date_to = datetime.date.max

    if request.values.get("time_from") and \
        len(request.values.get("time_from")) > 0:
        time_from = datetime.time(int(request.values.get("time_from")))
    else:
        time_from = datetime.time.min

    if request.values.get("time_to") and \
        len(request.values.get("time_to")) > 0:
        time_to = datetime.time(int(request.values.get("time_to")))
    else:
        time_to = datetime.time.max

    calorie = DataManager.get_calorie(calorie_id=calorie_id, 
        user_id=user_id, date_from=date_from, date_to=date_to, 
        time_from=time_from, time_to=time_to)

    # if results, set daytotal and whether the calorie falls on passing day
    if not type(calorie) is list:
        # single result
        (daytotal, meets) = utils.pass_fail_cal(calorie)
        sCal = calorie.serialize
        sCal["daytotal"] = daytotal
        sCal["meets"] = meets
        sCal["old_date"] = False
        sCal["old_date_meets"] = False
        sCal["old_date_daytotal"] = False
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
            sCal["old_date"] = False
            sCal["old_date_meets"] = False
            sCal["old_date_daytotal"] = False
            sCals.append(sCal)
        return jsonify(Data=sCals)
    else:
        # no results, return empty list
        return jsonify(Data=[])

@ccapp.route('/add_calorie', methods=['GET', 'POST'])
def add_calorie():
    """Endpoint for adding calorie records in the database.

    Args can be sent as key/value pairs in the query string ('GET'), or as
    key/value pairs in the content ('POST').
    All args are required.
    Args:
        user_id: the calorie's user id
        date: the calorie's date. must be given in 'YYYY-MM-DD' format
        time: the calorie's time. must be given as an hour, from 0 <= h <= 24
        text: the calorie's description
        amnt: the new number of calories
    Return:
        A JSON representing the database version(s) of the created calorie,
        with extra field representing the possibly new calorie total for that 
        day so the client may change pass/fail for any cached calories for that
        day.
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("user_id") and \
        len(request.values.get("user_id")) > 0:

        user_id = int(request.values.get("user_id"))
        if not utils.canCalorieCRUD(user_id, 
                login_session["user_id"], login_session["user_type_id"]):
            response = make_response(json.\
                dumps('Not authorized for cal actions for given user'), 403)
            response.headers['Content-Type'] = 'application/json'
            return response             
    else:
        response = make_response(json.dumps('Must provide valid user id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.values.get("date") and \
        len(request.values.get("date")) > 0:
        dates = bleach.clean(request.values.get("date")).split("-")
        date = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
        if not utils.is_calorie_date(date):
            response = make_response(json.\
                dumps('date invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        response = make_response(json.dumps('Must provide valid date'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.values.get("time") and \
        len(request.values.get("time")) > 0:
        time = datetime.time(int(request.values.get("time")))
        if not utils.is_calorie_time(time):
            response = make_response(json.\
                dumps('time invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        response = make_response(json.dumps('Must provide valid time'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.values.get("text") and \
        len(request.values.get("text")) > 0:
        text = bleach.clean(request.values.get("text"))
        if not utils.is_calorie_text(text):
            response = make_response(json.dumps('text invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        response = make_response(json.dumps('Must provide valid text'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.values.get("amnt") and \
        len(request.values.get("amnt")) > 0:
        amnt = request.values.get("amnt")
        if not utils.is_calorie_amount(amnt):
            response = make_response(json.dumps('amount invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        response = make_response(json.dumps('Must provide valid amount'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    cal_id = DataManager.add_calorie(user_id, date, time, text, amnt)
    calorie = DataManager.get_calorie(calorie_id=cal_id)

    if calorie:
        (daytotal, meets) = utils.pass_fail_cal(calorie)
        sCal = calorie.serialize
        sCal["daytotal"] = daytotal
        sCal["meets"] = meets
        sCal["old_date"] = False
        sCal["old_date_meets"] = False
        sCal["old_date_daytotal"] = False
        utils.pass_fail_cal(calorie)
        return jsonify(Data=[sCal])
    else:
        response = make_response(json.dumps('Internal server error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/edit_calorie', methods=['GET', 'POST'])
def edit_calorie():
    """Endpoint for editing calorie records in the database.

    Args can be sent as key/value pairs in the query string ('GET'), or as
    key/value pairs in the content ('POST').
    Args are optional unless noted.
    Args:
        calorie_id: the id of the calorie to edit (REQUIRED)
        user_id: the new user id
        date: the new date. must be given in 'YYYY-MM-DD' format
        time: the new time. must be given as an hour, from 0 <= h <= 24
        text: the new description
        num_calories: the new number of calories
    Return:
        A JSON representing the database version of the updated calorie,         
        with extra field representing the possibly new calorie total for that 
        day so the client may change pass/fail for any cached calories for that
        day.
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("calorie_id") and \
        len(request.values.get("calorie_id")) > 0:
        calorie_id = int(request.values.get("calorie_id"))
    else:
        response = make_response(json.dumps('Must provide calorie id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response  

    if request.values.get("user_id") and \
        len(request.values.get("user_id")) > 0:
        user_id = int(request.values.get("user_id"))
    else:
        user_id = None

    if request.values.get("date") and \
        len(request.values.get("date")) > 0:
        dates = bleach.clean(request.values.get("date")).split("-")
        date = datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))
        if not utils.is_calorie_date(date):
            response = make_response(json.\
                dumps('date invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        date = None

    if request.values.get("time") and \
        len(request.values.get("time")) > 0:
        time = datetime.time(int(bleach.clean(request.values.get("time"))))
        if not utils.is_calorie_time(time):
            response = make_response(json.\
                dumps('time invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        time = None

    if request.values.get("text") and \
        len(request.values.get("text")) > 0:
        text = bleach.clean(request.values.get("text"))
        if not utils.is_calorie_text(text):
            response = make_response(json.\
                dumps('text invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        text = None

    if request.values.get("amnt") and \
        len(request.values.get("amnt")) > 0:
        amnt = bleach.clean(request.values.get("amnt"))
        if not utils.is_calorie_amount(amnt):
            response = make_response(json.\
                dumps('amount invalid'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        amnt = None 

    # check permissions
    calorie = DataManager.get_calorie(calorie_id=calorie_id)
    if not utils.canCalorieCRUD(calorie.user_id, 
            login_session["user_id"], login_session["user_type_id"]):
        response = make_response(json.\
            dumps('Not authorized for cal actions for given user'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    if user_id and not utils.canCalorieCRUD(user_id, 
            login_session["user_id"], login_session["user_type_id"]):
        response = make_response(json.\
            dumps('Not authorized for cal actions for given user'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response 

    # get additional info
    old_calorie = DataManager.get_calorie(calorie_id=calorie_id)
    (old_daytotal, old_meets) = utils.pass_fail_cal(old_calorie)

    # make the update and return
    DataManager.edit_calorie(calorie_id, user_id=user_id, date=date,
        time=time, text=text, num_calories=amnt)
    calorie = DataManager.get_calorie(calorie_id=calorie_id)
    date_changed = old_calorie.date != calorie.date

    if calorie:
        (daytotal, meets) = utils.pass_fail_cal(calorie)
        sCal = calorie.serialize
        sCal["daytotal"] = daytotal
        sCal["meets"] = meets
        sCal["old_date"] = old_calorie.date
        sCal["old_date_meets"] = old_meets
        sCal["old_date_daytotal"] = old_daytotal
        return jsonify(Data=[sCal])
    else:
        response = make_response(json.dumps('Internal server error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response


@ccapp.route('/delete_calorie', methods=['GET', 'POST'])
def delete_calorie():
    """Endpoint for deleting calorie records from the database.

    Args can be sent as key/value pairs in the query string ('GET'), or as
    key/value pairs in the content ('POST').
    Args:
        calorie_id: the id of the calorie to delete (REQUIRED)
    Return:
        A JSON representing deletion success or failure, with success
        representing the possibly new calorie total for that day so the client 
        may change pass/fail for any cached calories for that day.
    """
    if not utils.is_logged_in():
        response = make_response(json.\
            dumps('Must sign in to CRUD'), 403)
        response.headers['Content-Type'] = 'application/json'

    if request.values.get("calorie_id") and \
        len(request.values.get("calorie_id")) > 0:

        calorie_id = int(request.values.get("calorie_id"))
        calorie = DataManager.get_calorie(calorie_id=calorie_id)

        # check permissions
        if not utils.canCalorieCRUD(calorie.user_id, 
                login_session["user_id"], login_session["user_type_id"]):

            response = make_response(json.\
                dumps('Not authorized for cal actions for given user'), 403)
            response.headers['Content-Type'] = 'application/json'
            return response

        # update and return
        (daytotal, meets) = utils.pass_fail_cal(calorie)
        date = calorie.date
        num_calories = DataManager.get_calorie(calorie_id).num_calories
        result = DataManager.delete_calorie(calorie_id)
        if result == 1:
            return jsonify({"Message": "Successful deletion",
                            "Post": "deletion",
                            "Model": "calorie",
                            "id": calorie_id,
                            "num_calories": num_calories,
                            "daytotal": daytotal,
                            "date": date,
                            "old_date": False,
                            "old_date_meets": False,
                            "old_date_daytotal": False})
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
    """Ajax endpoint for google sign in authentication.

    If successful, sets the secure session cookie with the authenticated
    user's information.

    REQUIRED: Google authorization code to be sent as 'data' in 
    the request content.
    Returns:
        A JSON with success or failure information.
    """
    # confirm entity with correct 3rd party credentials is same entity 
    # that is trying to login from the current login page's session.
    if request.values.get('state') != login_session['state']:
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
                    'user_type_id': login_session['user_type_id'],
                    'email': login_session['email'],
                    'exp_cal_day': login_session['exp_cal_day'],
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
                    'id': login_session['user_id'],
                    'user_type_id': login_session['user_type_id'],
                    'email': login_session['email'],
                    'exp_cal_day': login_session['exp_cal_day'],
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
