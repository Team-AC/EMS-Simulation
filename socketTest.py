import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:3000')
sio.wait()

sio.emit('my message', {'foo': 'bar'})