from datetime import datetime,timedelta
from threading import Timer

from modules.ev_module.real_time_data import real_time_data_start

def ev_simulation_init(sio):
    sio.sleep(1)

    real_time_data_start(sio)
    
    """ @sio.on('Generate Ev')
    def generate_ev(paramters_dict):
        lvl_2 = [0 for x in range(int(paramters_dict["num_ev_level_2"])]
        lvl_3 = [0 for x in range(int(paramters_dict["num_ev_level_3"])]
        real_time_data(pramters_dict, sio) """

    def generate_past_ev_data():
        ev_current_time = datetime.utcnow()
        ev_start_time_counter = ev_start_time = datetime.utcnow() - timedelta(hours=24) 
        
        
            
    generate_past_ev_data() 