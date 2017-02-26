# Use this script to repopulate the Calorie Count database
# WARNING: This script clears the database 'postgresql:///caloriecount.db'
from app.DataManager import drop_all_records, add_rows_from_json
from app.database_setup import UserType
import json


# delete everything
drop_all_records()


# populate db (e.g. add_rows_from_json(data))
tableConstructors = [UserType]

for tableConstructor in tableConstructors:
    dataObj = json.loads(open('initial_data/'+\
        tableConstructor.__name__+'.json', 'r').read())
    key = tableConstructor.__name__ + 's'
    data = dataObj[key]

    add_rows_from_json(data, tableConstructor)
