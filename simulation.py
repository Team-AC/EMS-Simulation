import socketio
import os
from simulation_modules.murb_module.murb_simulation import murb_simulation_init 
from simulation_modules.ev_module.ev_simulation import ev_simulation_init 
from simulation_modules.bess_module.bess_simulation import bess_simulation_init 

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

murb_simulation_init(sio)
ev_simulation_init(sio)
bess_simulation_init(sio)

sio.wait()