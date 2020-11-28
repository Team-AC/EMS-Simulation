from datetime import datetime, timedelta
import threading
import random
import socketio
import power_from_time

sio = socketio.Client()

my_date = datetime.now()
yesterday = datetime.now()-timedelta(1)
pst24 = yesterday
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

@sio.on('Old Murb Power Next')
def send_old_data():
    global counter
    global pst24
    global power
    if counter < (4 * 24):
        counter = counter + 1
        pst24 = pst24 + timedelta(0, 900)

        TimeStamp = pst24.isoformat()
        Power = power_from_time.power_from_time(pst24.now())
        sio.emit('Old Murb Power', {
            'TimeStamp': TimeStamp,
            'Power': Power
        })

def realTimeData():
    threading.Timer(900.0, realTimeData).start()

    TimeStamp = datetime.now().isoformat()
    Power = power_from_time.power_from_time(datetime.now())

    sio.emit('New Murb Power', {
        'TimeStamp': TimeStamp,
        'Power': Power
    })

data = []

sio.connect('http://localhost:3000')

send_old_data()
realTimeData()

