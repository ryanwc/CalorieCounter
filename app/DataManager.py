from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import (Base, User, UserType, Calorie)

import psycopg2 


def get_calorie_db_session():
    """Return an interactive session with the Calorie Count database.
    """
    engine = create_engine('postgresql+psycopg2://localhost/caloriecounter')
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


def add_user(username, email, google_id, exp_cal_day=None):
    """Add a user to the database.

    Args:
        username: the username of the user to add
        email: the email of the user to add
        google_id: the google account id of the user to add
        exp_cal_day: the number of calories the user expects
            to consume per day
    Returns:
        Returns the user id of the created user record
    """
    '''
    session = getCalorieDBSession()

    user = User(name=name, email=email)

    session.add(user)
    session.flush()
    user_id = user.id
    session.commit()
    session.close()

    return user_id'''


def add_user_type(name, CRUD_self, CRUD_users, CRUD_all):
    """Add a user type to the database.

    Args:
        name: the name of the user type to add
        CRUD_self: boolean, whether this user type can CRUD
            its own info and calorie entries
        CRUD_users: boolean, whether this user type can CRUD
            other users (but not their calories entries)
        CRUD_all: boolean, whether this user type can CRUD
            all info, including all users and all users'
            calorie entries
    Returns:
        The id of the created user type
    """


def add_calorie(user_id, date, time, text, num_calories):
    """Add a calorie record to the database.

    Args:
        user_id: the id of the user who consumed these calories
        date: the date these calories were consumed
        time: the time these calories were consumed
        text: the description of these calories
        num_calories: the number of calories consumed
    Returns:
        The id of created calorie record
    """


def get_user(user_id=None, username=None, email=None, google_id=None):
    """Return the user that matches the given arguments.

    Args:
        user_id: A list of user ids
        username: A list of usernames
        email: A list of email addresses
        google_id: A list of google account ids
    Returns:
        The user(s) specified by the arguments. If no arguments are given,
        returns all users.
    """
    '''
    session = getCalorieDBSession()

    if user_id is not None:
        user = session.query(User).filter_by(id=user_id).first()
    elif email is not None:
        user = session.query(User).filter_by(email=email).first()
    else:
        users = session.query(User).order_by(User.id).all()

    session.close()
    return user'''


def get_user_type(user_type_id=None, name=None, CRUD_self=None,
                  CRUD_users=None, CRUD_all=None):
    """Return the user type(s) that matches the given arguments.

    Args:
      user_type_id: A list of user type ids
      name: A list of user type names
      CRUD_self: whether the user type(s) to get can edit its own
        calorie entries
      CRUD_users: whether the user type to get can edit other
        users (but not their calorie entries)
      CRUD_all: whether the user type to get can edit all users and
        calorie entries
    Returns:
        The user type(s) specified by the arguments. If no arguments
        are given, returns all user types.
    """


def get_calorie(calorie_id=None, user_ids=None, user_types=None,
                date_from=None, date_to=None, time_from=None, time_to=None):
    """Get the calories record(s) matching the given arguments.

    Args:
        calorie_id: A list of calorie ids
        user_ids: A list of user ids
        date_from: A starting date
        date_to: An ending date
        time_from: A starting time
        time_to: An ending time
    Returns:
        The calorie(s) matching the given arguments. If no arguments are
        given, returns all calories.
    """


def edit_user(user_id, username=None, email=None,
              google_id=None, exp_cal_day=None):
    """Edit a user.
    Pass none for an attribute to leave it unchanged.

    Args:
        user_id: the id of the user to edit
        username: the new username
        email: the new email address
        google_id: the new google account id
        exp_cal_day: the new expected calorie count per day
    """
    '''
    session = getRestaurantDBSession()

    if newName is not None:
        session.query(User).filter_by(id=user_id).\
            update({'name':newName})

    session.commit()
    session.close()'''


def edit_user_type(user_type_id, name=None, CRUD_self=None,
                   CRUD_users=None, CRUD_all=None):
    """Edit a user type.
    Pass none for an attribute to leave it unchanged.

    Args:
        user_type_id: the id of the user type to edit
        name: the new name
        CRUD_self: the new boolean determining whether the user type can CRUD
            its own info and calorie entries
        CRUD_users: the new boolean determining whether the user type can
            CRUD other users' info (but not their calorie entries)
        CRUD_all: a new boolean determining whether the user
            can CRUD all users' info and calorie entries
    """


def edit_calorie(calorie_id, user_id=None, date=None, time=None,
                 text=None, num_calories=None):
    """Edit a calorie record.
    Pass none for an attribute to leave it unchanged.

    Args:
        calorie_id: the id of the calorie record to edit
        user_id: the new user id
        date: the new date
        time: the new time
        text: the new description
        num_calories: the new number of calories
    """


def delete_user(user_id):
    """Remove a user from the database.

    WARNING: This also deletes the user's calorie entries.

    Args:
        user_id: the id of the user to remove
    """
    '''
    session = getCalorieDBSession()

    calories = getCalories(user_id=user_id)

    for calorie in calories:
        deleteCalorie(calorie.id)

    session.query(User).filter_by(id=user_id).\
            delete(synchronize_session=False)

    session.commit()

    session.close()'''


def delete_user_type(user_type_id):
    """Remove a user type from the database.

    WARNING: This also deletes all of the users with this user type,
    which in turn deletes all of those users' calorie records.

    Args:
        user_type_id: the id of the user type to remove
    """


def delete_calorie(calore_id):
    """Remove a calorie record from the database.

    Args:
        calorie_id: the id of the calorie record to remove
    """


def add_rows_from_json(json_rows, table_constructor):
    """Convenience function: Populate the database from json-formatted data.
    Allows assigning specific values to auto-incremented columns, unlike the
    other add methods in this DAO.

    Args:
        json_rows: the rows to add in json format
        table_constructor: the Python constructor for the target table
    """
    '''
    session = getCalorieDBSession()
    
    for jsonRow in jsonRows:
        dbRow = tableConstructor(**jsonRow)
        session.add(dbRow)
        session.commit()

    session.close()'''


def drop_all_records():
    """Drop all records from the Calorie Count database
    """
    engine = create_engine('postgresql+psycopg2://localhost/caloriecounter')
    Base.metadata.bind = engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
