from datetime import datetime, timedelta, time
import threading
import random
import requests
import json
import socketio

sio = socketio.Client()

my_date = datetime.now()
yesterday = datetime.now()-timedelta(1)
pst24 = yesterday
counter = 0
power = 0

def is_time_between(check_time):
    power = 0

    if (check_time > time(21, 0, 0)) and (check_time < time(23, 59, 59)):
        power = 51 + (53 - 51)*random.random()
        return power

    if (check_time > time(16, 0, 0)) and (check_time < time(21, 0, 0)):
        power = 56 + (58 - 56)*random.random()
        return power

    if (check_time > time(13, 0, 0)) and (check_time < time(16, 0, 0)):
        power = 60 + (63 - 60)*random.random()
        return power

    if (check_time > time(9, 0, 0)) and (check_time < time(13, 0, 0)):
        power = 56 + (58 - 56)*random.random()
        return power

    if (check_time > time(5, 0, 0)) and (check_time < time(9, 0, 0)):
        power = 53 + (55 - 53)*random.random()
        return power

    if (check_time > time(0, 0, 0)) and (check_time < time(5, 0, 0)):
        power = 48 + (51 - 48)*random.random()
        return power

    return 0

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('Old Murb Power Next')
def send_old_data():
    global counter
    global pst24
    global power
    if counter < (4 * 24):
        counter = counter + 1
        pst24 = pst24 + timedelta(0, 900)

        TimeStamp = pst24.isoformat()
        Power = is_time_between(pst24.time())
        sio.emit('Old Murb Power', {
            'TimeStamp': TimeStamp,
            'Power': Power
        })

def realTimeData():
    threading.Timer(900.0, realTimeData).start()

    TimeStamp = datetime.now().isoformat()
    Power = is_time_between(datetime.now().time())

    url = 'http://localhost:3000/api/murb/newData'
    res = requests.post(url, json = {'TimeStamp': TimeStamp, "Power": Power})
    print("Response: ", res)

data = []

sio.connect('http://localhost:3000')

send_old_data()

