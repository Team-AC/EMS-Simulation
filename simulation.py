import socketio
from modules.murb_module.murb_simulation import murb_simulation_init 
from modules.ev_module.ev_simulation import ev_simulation_init 
from modules.bess_module.bess_simulation import bess_simulation_init 

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

# Initialize the simulations
murb_simulation_init(sio)
ev_simulation_init(sio)
bess_simulation_init(sio)

sio.connect('http://localhost:3000')

sio.wait()
