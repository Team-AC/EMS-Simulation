from datetime import datetime, timedelta, time
import threading
import random
import requests
import json
import socketio

sio = socketio.Client()

my_date = datetime.now()

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

dict_time_jump = {
    "pastDay": (4*24)-1,
    "pastWeek": (4*24*7)-1,
    "pastMonth": (4*24*30)-1,
    "pastYear": (4*24*365)-1
}

dict_time_delta = {
    "pastDay": 1,
    "pastWeek": 1*7,
    "pastMonth": 1*30,
    "pastYear": 1*365 
}

def realTimeData():
    global timer
    timer = threading.Timer(900.0, realTimeData)
    timer.start()
    TimeStamp = datetime.now().isoformat()
    Power = is_time_between(datetime.now().time())
    sio.emit('New Murb Power', {
        'TimeStamp': TimeStamp,
        'Power': Power
    })

@sio.on('Generate Murb Power')
def send_past_day(interval):
    global counter
    global power
    interval_start = datetime.now()-timedelta(dict_time_delta[interval])

    realTimeData()
    while counter < (dict_time_jump[interval]):
        counter = counter + 1
        interval_start = interval_start + timedelta(0, 900)
        TimeStamp = interval_start.isoformat()
        Power = is_time_between(interval_start.time())
        sio.emit('Old Murb Power', {
            'TimeStamp': TimeStamp,
            'Power': Power
        })
    
    counter = 0

@sio.on('Status Check')
def status_check():
    if 'timer' in globals():
        real_time_data_status = timer.is_alive()
    else:
        real_time_data_status = False

     
    return { 
        'real_time_data_status': real_time_data_status,
        'data_generate_config': dict_time_jump
    }


@sio.on('Pre - Generate Murb Power')
def pre_send_past_day():
    print("Received")


@sio.on('Stop Murb Power')
def stop_murb_data():
    global timer
    if 'timer' in globals():
        timer.cancel()

data = []

sio.connect('http://localhost:3002')

sio.wait()
