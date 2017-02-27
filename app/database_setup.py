import sys, psycopg2

from sqlalchemy import (Table, Column, ForeignKey, Integer, String, Date,
                        CheckConstraint, create_engine, Boolean, Time)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# create an object to hold the database's data
Base = declarative_base()


# define tables
class UserType(Base):
    """ORM mapping for SQL table 'user type' records.
    A 'user type' defines permissions for a user.
    """
    __tablename__ = 'user_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    CRUD_self = Column(Boolean, nullable=False)
    CRUD_users = Column(Boolean, nullable=False)
    CRUD_all = Column(Boolean, nullable=False)

    @property
    def serialize(self):
                return {
                        'id': self.id,
                        'name': self.name,
                        'CRUD_self': self.CRUD_self,
                        'CRUD_users': self.CRUD_users,
                        'CRUD_all': self.CRUD_all,
                }


class User(Base):
    """ORM mapping for SQL table 'user' records.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    exp_cal_day = Column(Integer, nullable=False)
    user_type_id = Column(Integer, ForeignKey('user_type.id'))

    user_type = relationship(UserType)

    CheckConstraint('exp_cal_day >= 0')

    @property
    def serialize(self):
                return {
                        'username': self.username,
                        'id': self.id,
                        'email': self.email,
                        'google_id': self.google_id,
                        'exp_cal_day': self.exp_cal_day,
                        'user_type': self.user_type,
                }


class Calorie(Base):
    """ORM mapping for SQL table 'calorie' records.
    """
    __tablename__ = 'calorie'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    text = Column(String(200), nullable=False)
    num_calories = Column(Integer, nullable=False)

    user = relationship(User)

    CheckConstraint('num_calories > 0')

    @property
    def serialize(self):
                return {
                        'id': self.id,
                        'user_id': self.user_id,
                        'date': self.date.isoformat(),
                        'time': self.time.isoformat(),
                        'text': self.text,
                        'num_calories': self.num_calories,
                }

# connect to database engine
engine = create_engine('postgresql+psycopg2://localhost/caloriecounter')

# creates the database as new tables with the given engine/name
Base.metadata.create_all(engine)
