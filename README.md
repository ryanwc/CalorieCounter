# Calorie Counter

A single-page web application for tracking calorie intake. Create entries with a date, time, description, and number of calories. Filter viewing entries by date and time of day. Set a daily expected calorie count and view which days fall below and above that count.

Users can CRUD their own calories, managers can CRUD their own calories and other users (except Admins), and admins can CRUD everything.

# Using the App

1. Navigate to to http://localhost:5000
2. Signin using your Google credentials.
3. Add, edit, or delete your calories. If you are a manager, add, edit or delete users. If you are an admin, add, edit, or delete all users and calories.

# Using the API

The backend provides all data necessary to run the application through endpoints that return JSON format objects.

Example use of a JSON endpoint is as follows:

1. Read the documentation for a specific endpoint to see which html query string parameters it accepts.
2. Pass the required and desired parameters in the html query string with the appropriate http method. For example, the documentation for the '/edit_user' endpoint notes that the 'user_id' argument is required, while there are several optional parameters. So, a valid query string for this endpoint is '/edit_user?user_id=[some user id][&optional arguments]'
3. Do what you need to with the received JSON.

The returned JSON will provide enough information to update any values cached on the client, so long as no other clients have changed server data values that correspond to the cached values.

In particular, on a change of user expected calories or change of number of calories in a day, a client should be able to update whether or not every cached calorie meets its owner's calorie expectations based on returned JSON data, so long as no other client has made changes to calorie amounts or made changes to user expected calorie totals.

## Signin and Authentication 

You must have valid login credentials to get any data from the API. So, it is recommended to imlpement a Google OAuth system on your front-end that sends and authorization code to the '/gconnect' endpoint, which will grant access to the API if the authorization code can be exchanged for login credentials.

# Technologies Used

- Python Flask backend
- AngularJS frontend 

# Requirements

bleach==1.4.3
Flask==0.12
Flask_Cors==3.0.2
Flask_RESTful==0.3.5
httplib2==0.9.2
psycopg2==2.6.2
requests==2.10.0
SQLAlchemy==1.0.12
google_api_python_client==1.6.2

# License

Created by Ryan William Connor in February 2017.  
Copyright © 2017 Ryan William Connor. All rights reserved.