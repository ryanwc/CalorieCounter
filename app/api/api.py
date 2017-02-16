from flask import Blueprint, jsonify
import app.DataManager, app

api_bp = Blueprint('api', __name__)


@app.route('/user_type/JSON/')
def user_type_json():
    """JSON endpoint for serving user type data from the database.
    """
    #data = DataManager.getData()

    #return jsonify(Data=[i.serialize for i in data])


@app.route('/user/<int:user_id>/JSON/')
def user_json(user_id):
    """JSON endpoint for serving user data from the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)

@app.route('/calorie/<int:calorie_id>/JSON/')
def calorie_json(calorie_id):
    """JSON endpoint for serving calorie record data from the database.
    """
    #data = DataManager.getData(id)

    #return jsonify(Data=data.serialize)
