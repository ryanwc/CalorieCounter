from flask import Blueprint, jsonify
from app import DataManager, ccapp

api_bp = Blueprint('api', __name__)


@ccapp.route('/user_type/JSON/')
def user_type_json():
    """JSON endpoint for serving user type data from the database.
    """
    #data = DataManager.getData()

    #return jsonify(Data=[i.serialize for i in data])


@ccapp.route('/user/<int:user_id>/JSON/')
def user_json(user_id):
    """JSON endpoint for serving user data from the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)

@ccapp.route('/calorie/<int:calorie_id>/JSON/')
def calorie_json(calorie_id):
    """JSON endpoint for serving calorie record data from the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)
