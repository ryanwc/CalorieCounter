from flask import flash, session as login_session

from . import ccapp, DataManager

import bleach, json, re, datetime


def pass_fail_cal(calorie):
    """Determine whether this is a pass or fail calorie based on
    the user's daily calorie limit.
    """
    # get total for cal's day
    print "passing or failing cals"
    user = DataManager.get_user(user_id=calorie.user_id)
    cals_on_day = DataManager.get_calorie(user_id=user.id, 
        date_from=calorie.date, date_to=calorie.date)
    print cals_on_day
    daytotal = 0
    for cal in cals_on_day:
        print "adding "
        print cal.num_calories
        daytotal += cal.num_calories

    # (met if no exp_total set)
    meets = daytotal <= user.exp_cal_day or user.exp_cal_day == 0
    print "finished"
    print daytotal
    print meets
    return daytotal, meets

def canSetPermissions(cruder_user_type_id):
    """Return whether the cruder_user_id in user has permissions to set
    user permissions.
    """
    return DataManager.get_user_type(user_type_id=cruder_user_type_id).CRUD_all

def canCalorieCRUD(user_id, cruder_user_id, cruder_user_type_id):
    """Return whether the cruder_user_id in user has permissions for calorie 
    actions on calories owned by user_id.
    """
    return user_id == cruder_user_id or \
            DataManager.get_user_type(user_type_id=cruder_user_type_id).CRUD_all

def canUserCRUD(user_id, cruder_user_id, cruder_user_type_id):
    """Return whether the cruder_user_id in user has permissions for user profile 
    actions on user_id.
    """
    return user_id == cruder_user_id or \
            DataManager.get_user_type(user_type_id=cruder_user_type_id).CRUD_users

def is_logged_in():
    """Return true if the user is logged in, false otherwise.
    """
    return ('credentials' in login_session and
            'access_token' in login_session['credentials'] and
            'user_id' in login_session)

def set_session_user_info():
    """Populate the login session with the logged in user's settings.
    """
    user = DataManager.get_user(email=login_session['email'])

    # create the user if the user doesn't exist
    if user is None:
        DataManager.add_user(username=login_session['username'],
                             email=login_session['email'])
        user = DataManager.get_user(email=login_session['email'])

    login_session['user_id'] = user.id
    login_session['username'] = user.username
    login_session['user_type_id'] = user.user_type_id
    login_session['exp_cal_day'] = user.exp_cal_day


def get_client_login_session():
    """Return a dict with entries for setting dynamic client-side content
    """
    client_login_session = {}
    client_login_session['username'] = ""
    client_login_session['user_id'] = -99
    client_login_session['message'] = "Not logged in"

    if is_logged_in():

        client_login_session['username'] = login_session['username']
        client_login_session['user_id'] = login_session['user_id']
        client_login_session['message'] = "Logged in as " + \
            login_session['username']

    return client_login_session


# form validation

def is_csrf_attack(current_state):
    """Validate the request came from the same session that logged in
    at the homepage.
    """
    if current_state != login_session['state']:
        flash("An unknown error occurred. Sorry! Try signing out, " +
              "signing back in, and repeating the operation.")
        return True
    else:
        return False


def validate_user_input(user_input, col_name, crud_type, item_msg_name,
                        col_msg_name=None, maxlength=None, required=False,
                        unique=False, old_input=None, table_name=None,
                        valid_inputs=None, username_format=False):
    """Validate (and strip HTML) from user input.

    Returns the validated input, or none with a flashed message
    if the test fails.

    Args:
        user_input: the input to validate
        col_name: the name of the database column for this input
        col_msg_name: the name of the columm for user message.
            Pass None if same as column_name.
        crud_type: create, read, update, or delete
        item_msg_name: the name for this item in response text to the user
        maxlength: the max allowable length of this input
        required: true if form submission requires this input
        unique: whether this input needs to be unique in the table
        old_input: for an edit -- the value to replace
        table_name: only needed if unique is True
        valid_inputs: dictionary with keys that are the only valid inputs
        username_format: true if the input should be a legal username
    """
    # TO-DO: break into helper functions, validate Calorie Counter specific data
    if not col_msg_name:
        col_msg_name = col_name

    bad_result = "Did not " + crud_type + " " + item_msg_name + ". "
    neutral_result = "Did not edit " + col_msg_name + ". "

    if not user_input or len(user_input) < 1:

        if required:
            flash(bad_result + "Must provide a " + col_msg_name + ".")
        else:
            flash(neutral_result + "Nothing provided.")

        return None

    user_input = bleach.clean(user_input)

    if user_input and maxlength:
        if len(user_input) > maxlength:

            if required:
                flash(bad_result + col_msg_name + "was too long.")
            else:
                flash(neutral_result + "It was too long.")

            return None

    if user_input and unique:
        if not is_unique(user_input, col_name, table_name):
            
            if required:
                flash(bad_result + col_msg_name + " was not unique.")
            else:
                flash(neutral_result + "It was not unique.")
            return None

    if user_input and old_input:
        if user_input == old_input:

            if required:
                flash(bad_result+col_msg_name+" provided was same as before")
            else:
                flash(neutral_result + \
                    "The one provided was the same as before.")

            return None

    if user_input and valid_inputs:
        if user_input not in valid_inputs:

            if required:
                flash(bad_result+col_msg_name+" was not a valid selection")
            else:
                flash(neutral_result + "It was not a valid selection.")

            return None

    if user_input and username_format:
        match = \
            re.search(r"[^~`!@#\$%\^&\*\(\)_=\+\{}\[\]\\\|\.<>\?/;:]\+",
                user_input)
        if match is not None:

            if required:
                flash(bad_result+col_msg_name+" had an illegal character.")
            else:
                flash(neutral_result + "It had an illegal character.")

            return None

    return user_input


def is_unique(value, col_name, table_name):
    """Return true if value is unique for a column within a table.
    """
    same_value = False

    if table_name == 'User':
        if col_name == 'username':
            same_value = DataManager.get_user(username=value)
    elif table_name == 'user_type':
        if col_name == 'UserType':
            same_value = DataManager.get_user_type(name=value)

    return not same_value


def is_username(username):
    """ Return whether the given argument is a valid username
    """
    return len(str(username)) < 31


def is_email(email):
    """ Return whether the given argument is a valid email address
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def is_exp_cal(exp_cal_day):
    """ Return whether the given argument is a valid exp_cal_day
    """
    return int(exp_cal_day) > -1 and int(exp_cal_day) < 20000


def is_calorie_date(date):
    """ Return whether the given argument is a valid date
    """
    return isinstance(date, datetime.date)


def is_calorie_time(time):
    """ Return whether the given argument is a valid time
    """
    return isinstance(time, datetime.time)

def is_calorie_amount(num):
    """
    """
    return int(num > 0)


def is_calorie_text(text):
    """
    """
    return len(str(text)) < 201


def is_user_type_id(id):
    """
    """
    user_type = DataManager.get_user_type(user_type_id=id)
    if user_type:
        return True
    else:
        return False

