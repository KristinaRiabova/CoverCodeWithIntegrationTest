import requests
import time
from datetime import datetime
from flask import Flask, jsonify, request
import threading
from data_loader import update_user_data, user_data_storage

user_data_storage = {}
date_format = "%Y-%m-%dT%H:%M"
app = Flask(__name__)


def format_date_string(date_string):
    dash_count = 0
    formatted_date_string = ''
    for char in date_string:
        if char == '-':
            dash_count += 1
        if dash_count == 3:
            formatted_date_string += 'T'
            dash_count = 0
        else:
            formatted_date_string += char


    try:
        datetime.strptime(formatted_date_string, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise ValueError("Invalid date string format")

    return formatted_date_string


date_format = "%Y-%m-%dT%H:%M"
user_data_storage = {}




@app.route('/user_intervals', methods=['GET'])
def get_user_intervals():
    return jsonify(user_data_storage)

@app.route('/api/stats/users', methods=['GET'])
def get_users_online():

    date_str = format_date_string(request.args.get('date'))


    date = datetime.strptime(date_str, date_format)

    date = date.replace(second=0)

    online_users = count_online_users(date)
    return jsonify({"usersOnline": online_users})


def count_online_users(date):
    online_users = 0
    print(date)

    for user_id, intervals in user_data_storage.items():
        for interval in intervals:
            start_time, end_time = interval


            print(f"Checking interval: {start_time} - {end_time}")


            if not isinstance(start_time, datetime):
                start_time = datetime.strptime(start_time, date_format)
            if end_time and not isinstance(end_time, datetime):
                end_time = datetime.strptime(end_time, date_format)


            end_time = end_time or datetime.now()


            if end_time <= date <= start_time:
                online_users += 1

    return online_users




if __name__ == '__main__':

    data_update_thread = threading.Thread(target=update_user_data)
    data_update_thread.daemon = True
    data_update_thread.start()



    app.run(debug=True)
