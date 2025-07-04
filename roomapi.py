from flask import Flask, jsonify, request
from pathlib import Path
from parsecsv import *
import os
from time import sleep
try: import env
except: pass

try:
    xxxx = os.environ['no-delay-key']
except:
    print('No key in environment')
    try: xxxx = env.no_delay_key
    except:
        print('null key')
        xxxx = 'null'

app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):

        key = request.args.get('no-delay-key', -1)
        if key != xxxx: sleep(3)

        data = [
            {"Action": "Help", "Format" : "/?no-delay-key=--OPTIONAL--KEY--"},
            {"Action": "List all rooms", "Format" : "/list-rooms&no-delay-key=--OPTIONAL--KEY--"},
            {"Action": "Fetch data for room", "Format" : "/fetch-room?roomname=D217&no-delay-key=--OPTIONAL--KEY--"},
            {"Action" : "Check if room is available during a given instant on a specific day", "Format" : "/check-instant?roomname=D217&day=Mon&time=01:00 PM&no-delay-key=--OPTIONAL--KEY--"},
            {"Action" : "Check if room is available during a given interval on a specific day", "Format" : "/check-interval?roomname=D217&day=Mon&starttime=09:00 AM&endtime=01:00 PM&no-delay-key=--OPTIONAL--KEY--"},
            {"Action" : "List all available rooms during a given instant on a specific day", "Format" : "/list-instant?day=Mon&time=01:00 PM&no-delay-key=--OPTIONAL--KEY--"},
            {"Action" : "List all available rooms during a given interval on a specific day", "Format" : "/list-interval?day=Mon&starttime=09:00 AM&endtime=01:00 PM&no-delay-key=--OPTIONAL--KEY--"},
        ]
        return jsonify(data)
    
@app.route('/list-rooms', methods = ['GET', 'POST'])
def list_rooms():
    if(request.method == 'GET'):
        key = request.args.get('no-delay-key', -1)
        if key != xxxx: sleep(3)
        data = csv_result['roomset']
        return jsonify({"Rooms":data})

@app.route('/fetch-room', methods = ['GET', 'POST'])
def fetch_room():
    if(request.method == 'GET'):
        input_string = request.args.get("roomname")
        key = request.args.get('no-delay-key', -1)
        if key != xxxx: sleep(3)

        data = fetchroom(input_string).dict()
        return jsonify({"Result":data})

@app.route('/check-instant', methods = ['GET', 'POST'])
def check_instant():
    if(request.method == 'GET'):
        roomname = request.args.get("roomname")
        day = request.args.get("day")
        time = request.args.get("time")
        key = request.args.get('no-delay-key', -1)
        if key != xxxx: sleep(3)

        data = fetchroom(roomname).checkinstant(day, time)
        return jsonify({"roomname":roomname, "day" : day, 'time': time, 'available' : data})

@app.route('/check-interval', methods = ['GET', 'POST'])
def check_interval():
    if(request.method == 'GET'):
        roomname = request.args.get("roomname")
        day = request.args.get("day")
        starttime = request.args.get("starttime")
        endtime = request.args.get("endtime")
        print(roomname, day, starttime, endtime)
        key = request.args.get('no-delay-key', -1)
        if key != xxxx: sleep(3)

        
        data = fetchroom(roomname).checkinterval(day, starttime, endtime)
        return jsonify({"roomname":roomname, "day" : day, 'interval': starttime+' - '+endtime, 'available' : data})
    

@app.route('/list-instant', methods = ['GET', 'POST'])
def list_instant():
    if(request.method == 'GET'):
        day = request.args.get("day")
        time = request.args.get("time")
        key = request.args.get('no-delay-key', -1)
        if key != xxxx: sleep(3)

        data = [i for i in csv_result['roomset'] if fetchroom(i).checkinstant(day, time)]
        return jsonify({"day" : day, 'time': time, 'available' : data})

@app.route('/list-interval', methods = ['GET', 'POST'])
def list_interval():
    if(request.method == 'GET'):
        day = request.args.get("day")
        starttime = request.args.get("starttime")
        endtime = request.args.get("endtime")

        key = request.args.get('no-delay-key', -1)
        if key != xxxx: sleep(3)

        
        data = [i for i in csv_result['roomset'] if fetchroom(i).checkinterval(day, starttime, endtime)]
        return jsonify({"day" : day, 'interval': starttime+' - '+endtime, 'available' : data})

# Run with gunicorn -w 1 roomapi:app

# driver function
if __name__ == '__main__':

    app.run(debug=True)