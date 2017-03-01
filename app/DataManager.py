from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import (Base, User, UserType, Calorie)

import datetime

import psycopg2 


def get_calorie_db_session():
    """Return an interactive session with the Calorie Count database.
    """
    engine = create_engine('postgresql+psycopg2://localhost/caloriecounter')
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


def add_user(username, email, exp_cal_day=None, user_type_id=None):
    """Add a user to the database.

    Args:
        username: the username of the user to add
        email: the email of the user to add
        exp_cal_day: the number of calories the user expects
            to consume per day
        user_type_id: the user type for the user to add
    Returns:
        Returns the user id of the created user record
    """
    session = get_calorie_db_session()

    if user_type_id is None:
        user_type_id = get_user_type(CRUD_self=True, 
            CRUD_users=False, CRUD_all=False)[0].id

    if not exp_cal_day:
        exp_cal_day = 0

    user = User(username=username, email=email, exp_cal_day=exp_cal_day, 
        user_type_id=user_type_id)

    session.add(user)
    session.flush()
    user_id = user.id
    session.commit()
    session.close()

    return user_id


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
    session = get_calorie_db_session()

    user_type = UserType(name=name, CRUD_self=CRUD_self, 
        CRUD_users=CRUD_users, CRUD_all=CRUD_all)

    session.add(user_type)
    session.flush()
    user_type_id = user_type.id
    session.commit()
    session.close()

    return user_type_id    


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
    session = get_calorie_db_session()

    calorie = Calorie(user_id=user_id, date=date, time=time, text=text, 
        num_calories=num_calories)

    session.add(calorie)
    session.flush()
    calorie_id = calorie.id
    session.commit()
    session.close()

    return calorie_id


def get_user(user_id=None, username=None, email=None):
    """Return the user that matches the given arguments.

    Args:
        user_id: A user id
        username: A username
        email: An email address
    Returns:
        The user specified by the arguments. If no arguments are given,
        returns all users.
    """
    session = get_calorie_db_session()

    if user_id is not None:
        user = session.query(User).filter_by(id=user_id).first()
    elif email:
        user = session.query(User).filter_by(email=email).first()
    else:
        user = session.query(User).order_by(User.id).all()

    print user
    session.close()
    return user


def get_user_type(user_type_id=None, name=None, CRUD_self=None,
                  CRUD_users=None, CRUD_all=None):
    """Return the user type(s) that matches the given arguments.

    Args:
      user_type_id: A user type id
      name: A user type name
      CRUD_self: whether the user type(s) to get can edit its own
        calorie entries
      CRUD_users: whether the user type(s) to get can edit other
        users (but not their calorie entries)
      CRUD_all: whether the user type to get can edit all users and
        calorie entries
    Returns:
        The user type(s) specified by the arguments. If no arguments
        are given, returns all user types.
    """
    session = get_calorie_db_session()

    if user_type_id is not None:
        user_type = session.query(UserType).filter_by(id=user_type_id).first()
    elif name:
        user_type = session.query(UserType).filter_by(name=name).first()
    elif CRUD_self:
        user_type = session.query(UserType).filter_by(CRUD_self=True).all()
    elif CRUD_users:
        user_type = session.query(UserType).filter_by(CRUD_users=True).all()
    elif CRUD_all:
        user_type = session.query(UserType).filter_by(CRUD_all=True).all()
    else:
        user_type = session.query(UserType).order_by(UserType.id).all()

    session.close()
    return user_type


def get_calorie(calorie_id=None, user_id=None, user_type_id=None,
                date_from=datetime.date.min, date_to=datetime.date.max, 
                time_from=datetime.time.min, time_to=datetime.time.max):
    """Get the calories record(s) matching the given arguments.
    Defaults to returning calories recorded at all possible date and times.

    Args:
        calorie_id: A calorie id
        user_id: A user id
        date_from: A starting date
        date_to: An ending date
        time_from: A starting time
        time_to: An ending time
    Returns:
        The calorie(s) matching the given arguments. If no arguments are
        given, returns all calories.
    """
    session = get_calorie_db_session()

    print "getting cals from "
    print user_id
    print date_from
    print date_to

    if calorie_id is not None:
        calorie = session.query(Calorie).filter_by(id=calorie_id).first()
    elif user_id is not None:
        calorie = session.query(Calorie).\
            filter(Calorie.user_id == user_id,
                   Calorie.date >= date_from,
                   Calorie.date <= date_to,
                   Calorie.time >= time_from,
                   Calorie.time <= time_to).all()
    elif user_type_id is not None:
        calorie = session.query(Calorie).\
            filter(Calorie.user_type_id == user_type_id,
                   Calorie.date >= date_from,
                   Calorie.date <= date_to,
                   Calorie.time >= time_from,
                   Calorie.time <= time_to).all()
    else:
        calorie = session.query(Calorie).\
            filter(Calorie.date >= date_from,
                   Calorie.date <= date_to,
                   Calorie.time >= time_from,
                   Calorie.time <= time_to).all()

    session.close()
    return calorie

def edit_user(user_id, username=None, email=None, exp_cal_day=None):
    """Edit a user.
    Pass none for an attribute to leave it unchanged.

    Args:
        user_id: the id of the user to edit
        username: the new username
        email: the new email address
        exp_cal_day: the new expected calorie count per day
    """
    session = get_calorie_db_session()

    user = session.query(User).filter_by(id=user_id).first()

    if username:
        user.username = username
    
    if email:
        user.email = email
    
    if exp_cal_day:
        user.exp_cal_day = exp_cal_day

    session.commit()
    session.close()


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
    session = get_calorie_db_session()

    user_type = session.query(UserType).filter_by(id=user_type_id).first()

    if name:
        user_type.name = name
    
    if CRUD_self:
        user_type.CRUD_self = CRUD_self
    
    if CRUD_users:
        user_type.CRUD_users = CRUD_users

    if CRUD_all:
        user_type.CRUD_all = CRUD_all

    session.commit()
    session.close()

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
    session = get_calorie_db_session()

    calorie = session.query(Calorie).filter_by(id=calorie_id).first()

    if user_id is not None:
        calorie.user_id = user_id
    
    if date:
        calorie.date = date
    
    if time:
        calorie.time = time

    if text:
        calorie.text = text

    if num_calories:
        calorie.num_calories = num_calories

    session.commit()
    session.close()

def delete_user(user_id):
    """Remove a user from the database.

    WARNING: This also deletes the user's calorie entries.

    Args:
        user_id: the id of the user to remove
    Return:
        sqlalchemy result object of query
    """
    session = get_calorie_db_session()

    calories = get_calorie(user_id=user_id)

    for calorie in calories:
        delete_calorie(calorie.id)

    result = session.query(User).\
        filter_by(id=user_id).delete(synchronize_session=False)

    session.commit()
    session.close()
    return result


def delete_user_type(user_type_id):
    """Remove a user type from the database.

    WARNING: This also deletes all of the users with this user type,
    which in turn deletes all of those users' calorie records.

    Args:
        user_type_id: the id of the user type to remove
    Return:
        sqlalchemy result object of query
    """
    session = get_calorie_db_session()

    users = get_user(user_type_id=user_type_id)

    for user in users:
        delete_user(user.id)

    result = session.query(UserType).filter_by(id=user_type_id).\
        delete(synchronize_session=False)

    session.commit()
    session.close()
    return result

def delete_calorie(calorie_id):
    """Remove a calorie record from the database.

    Args:
        calorie_id: the id of the calorie record to remove
    Return:
        sqlalchemy result object of query
    """
    session = get_calorie_db_session()

    result = session.query(Calorie).filter_by(id=calorie_id).\
        delete(synchronize_session=False)

    session.commit()
    session.close()
    return result

def add_rows_from_json(json_rows, table_constructor):
    """Convenience function: Populate the database from json-formatted data.
    Allows assigning specific values to auto-incremented columns, unlike the
    other add methods in this DAO.

    Args:
        json_rows: the rows to add in json format
        table_constructor: the Python constructor for the target table
    """
    session = get_calorie_db_session()
    
    for json_row in json_rows:
        db_row = table_constructor(**json_row)
        session.add(db_row)
        session.commit()

    session.close()


def drop_all_records():
    """Drop all records from the Calorie Count database
    """
    engine = create_engine('postgresql+psycopg2://localhost/caloriecounter')
    Base.metadata.bind = engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
