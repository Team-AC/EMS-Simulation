from datetime import datetime,timedelta
from threading import Timer

from simulation_modules.ev_module.real_time_data import real_time_data_start
from simulation_modules.ev_module.historical_data import historical_data

global use_bess

def ev_simulation_init(sio):
    sio.sleep(1)

    @sio.on('Generate Ev')
    def generate_ev(interval, ev_parameters_dict, bess_parameters_dict):
        historical_data(interval, ev_parameters_dict, bess_parameters_dict, sio)
        # real_time_data_start(ev_parameters_dict, sio)
        
