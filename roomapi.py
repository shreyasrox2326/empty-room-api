from flask import Flask, jsonify, request
from pathlib import Path
from parsecsv import *


app = Flask(__name__)
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):

        data = [
            {"Action": "List all rooms", "Format" : "/list-rooms"},
            {"Action": "Fetch data for room", "Format" : "/fetch-room?roomname=D217"},
            {"Action" : "Check if room is available during a given instant on a specific day", "Format" : "/check-instant?roomname=D217&day=Mon&time=01:00 PM"},
            {"Action" : "Check if room is available during a given interval on a specific day", "Format" : "/check-interval?roomname=D217&day=Mon&starttime=09:00 AM&endtime=01:00 PM"}
        ]
        return jsonify(data)
    
@app.route('/list-rooms', methods = ['GET', 'POST'])
def list_rooms():
    if(request.method == 'GET'):

        data = csv_result['roomset']
        return jsonify({"Rooms":data})

@app.route('/fetch-room', methods = ['GET', 'POST'])
def fetch_room():
    if(request.method == 'GET'):
        input_string = request.args.get("roomname")

        data = fetchroom(input_string).dict()
        return jsonify({"Result":data})

@app.route('/check-instant', methods = ['GET', 'POST'])
def check_instant():
    if(request.method == 'GET'):
        roomname = request.args.get("roomname")
        day = request.args.get("day")
        time = request.args.get("time")

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

        
        data = fetchroom(roomname).checkinterval(day, starttime, endtime)
        return jsonify({"roomname":roomname, "day" : day, 'interval': starttime+' - '+endtime, 'available' : data})
    
    


# Run with gunicorn -w 1 -b 127.0.0.1:5000 roomapi:app

# driver function
if __name__ == '__main__':

    app.run(debug=True)