from datetime import datetime,timedelta
from threading import Timer

from modules.ev_module.real_time_data import real_time_data_start

def ev_simulation_init(sio):
    sio.sleep(1)

    @sio.on('Generate Ev')
    def generate_ev(paramters_dict):
        real_time_data_start(sio)