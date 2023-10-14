import requests
import time
from datetime import datetime
from flask import Flask, jsonify, request, abort
import threading
from data_loader import update_user_data, user_data_storage

date_format = "%Y-%m-%dT%H:%M"
user_data_storage = {}
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
    return formatted_date_string




@app.route('/api/stats/user', methods=['GET'])
def get_user_historical_data():

    date_str = request.args.get('date')
    user_id = request.args.get('userId')


    if user_id not in user_data_storage:
        return abort(404)


    date = datetime.strptime(format_date_string(date_str), date_format)


    was_user_online = False
    nearest_online_time = None


    intervals = user_data_storage[user_id]
    for interval in intervals:
        start_time, end_time = interval

        if not isinstance(start_time, datetime):
            start_time = datetime.strptime(start_time, date_format)
        if end_time and not isinstance(end_time, datetime):
            end_time = datetime.strptime(end_time, date_format)


        if (end_time or datetime.now()) <= date <= start_time:
            was_user_online = True
            nearest_online_time = None
            break


        if nearest_online_time is None or abs(date - start_time) < abs(date - nearest_online_time):
            nearest_online_time = start_time




    response_data = {
        "wasUserOnline": was_user_online,  # Set to True if user was online
        "nearestOnlineTime": nearest_online_time.strftime(date_format) if nearest_online_time else None
    }

    return jsonify(response_data)


@app.route('/user_intervals', methods=['GET'])
def get_user_intervals():
    return jsonify(user_data_storage)

if __name__ == '__main__':
    data_update_thread = threading.Thread(target=update_user_data)
    data_update_thread.daemon = True
    data_update_thread.start()
    app.run(debug=True)

