import socketio
import os
from simulation_modules.simulation import simulation_init
from design_modules.design import design_init
from optimization_modules.optimization import optimization_init

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


# Connect to port 80 in production and 3000 in development
if ('PROD' in os.environ) and (int(os.environ['PROD']) == 1):
    sio.connect('http://localhost:80')
else:
    sio.connect('http://localhost:3000')

simulation_init(sio)
design_init(sio)
optimization_init(sio)

sio.wait()
