from datetime import datetime, timedelta
import threading
import random
import socketio
import power_from_time_model

sio = socketio.Client()

my_date = datetime.now()

counter = 0
power = 0

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
    "pastDay": 4*24,
    "pastWeek": 4*24*7,
    "pastMonth": 4*24*30,
    "pastYear": 4*24*365
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
    Power = power_from_time_model.power_from_time_model(datetime.now().time())
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
        Power = power_from_time_model.power_from_time_model(interval_start.time())

        sio.emit('Old Murb Power', {
            'TimeStamp': TimeStamp,
            'Power': Power
        })
    
    counter = 0

@sio.on('Pre - Generate Murb Power')
def pre_send_past_day():
    print("Received")


@sio.on('Stop Murb Power')
def stop_murb_data():
    global timer
    if 'timer' in globals():
        timer.cancel()

data = []

sio.connect('http://localhost:3000')

sio.wait()
