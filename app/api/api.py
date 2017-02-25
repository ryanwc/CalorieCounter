from flask import Flask, Blueprint, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from app import DataManager, ccapp

api_bp = Blueprint('api', __name__)
Api(ccapp)
CORS(ccapp)

# endpoints

@ccapp.route('/user_type/JSON/', methods=['GET'])
def user_type_json():
    """JSON endpoint for serving user type data from the database.
    """
    #data = DataManager.getData()

    #return jsonify(Data=[i.serialize for i in data])


@ccapp.route('/user/<int:user_id>/JSON/', methods=['GET'])
def user_json(user_id):
    """JSON endpoint for serving user data from the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)

@ccapp.route('/calorie/<int:calorie_id>/JSON/', methods=['GET'])
def calorie_json(calorie_id):
    """JSON endpoint for serving calorie record data from the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)

@ccapp.route('/signin', methods=['POST'])
def signin():
    """Endpoint for signing in to Calorie Counter app.
    """
    data = request.json
    print "hi" 
    return jsonify({'username':data['username'],
                    'password':data['password'], 
                    'Access-Control-Allow-Origin': '*'})

@ccapp.route('/signout/', methods=['POST'])
def signout():
    """Endpoint for signing out of Calorie Counter app.
    """

