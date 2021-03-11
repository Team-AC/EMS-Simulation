from datetime import timedelta, datetime, timezone
from threading import Timer
from simulation_modules.ev_module.check_ev_coming_in_to_charge import check_ev_coming_in_to_charge
from simulation_modules.ev_module.logic_ev_charger_check import logic_ev_charger_check
from simulation_modules.ev_module.check_ev_levels_chargers import check_ev_level_2_charger, check_ev_level_3_charger


#Real Time Data
def end_charging(charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use, lvl_2, lvl_3):
    in_use = 0
    if ev_start_time != 0:
        if ev_charger_level == 2:
            lvl_2[int(ev_charger_num)] = in_use
            #print("lvl 2",lvl_2)
        else:
            lvl_3[int(ev_charger_num)] = in_use
            #print("lvl 3",lvl_3)
        #print("charging done and it good to use again")
        
        ev_time_stamp = ev_start_time + timedelta(seconds=charge_time*3600)

        sio.emit('New EV Power', {
            'TimeStamp': ev_time_stamp.isoformat(),
            'Power': power,
            'ChargeTime': charge_time,
            'EvChargerNumber': ev_charger_num,
            'EvChargerType': ev_charger_level
        })
#Real Time Data
def start_charging(charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use, lvl_2, lvl_3):
    charge_time_in_sec = charge_time*3600
    Timer(charge_time_in_sec, end_charging, (charge_time, power,ev_charger_num, ev_charger_level, ev_start_time, in_use, lvl_2, lvl_3)).start()



#lvl_2 = [0 for x in range(3)]
#lvl_3 = [0 for x in range(3)]

def real_time_data(parameter_dict): #(paramter_dict, sio)
    global lvl_2
    global lvl_3
    global timer

    ev_start_time = datetime.now(timezone.utc)
    ev_wanting_charge, ev_battery_start_percentage = check_ev_coming_in_to_charge(ev_start_time, parameter_dict)
    charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use = logic_ev_charger_check(ev_wanting_charge, ev_battery_start_percentage, ev_start_time, lvl_2, lvl_3, parameter_dict)
    start_charging(charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use, lvl_2, lvl_3)
    timer = Timer(30, real_time_data, (parameter_dict,))
    timer.start()


def real_time_data_start(parameter_dict, sio_passed_in):
    global sio
    global lvl_2
    global lvl_3
    lvl_2 = [0 for x in range(int(parameter_dict['numOfEvLevel2']))]
    lvl_3 = [0 for x in range(int(parameter_dict['numOfEvLevel3']))]
    sio = sio_passed_in
    real_time_data(parameter_dict)


    @sio.on('Stop Ev Power')
    def stop_ev_data():
        if 'timer' in globals():
            timer.cancel()


    @sio.on('Status Check Ev')
    def status_check_ev():
        if 'timer' in globals():
            real_time_data_status = timer.is_alive()
        else:
            real_time_data_status = False
            
        return {
            'real_time_data_status': real_time_data_status
        }


    @sio.on('Status Check Ev Chargers')
    def status_check_ev_charger():
        return {
            'lvl_2_statuses': lvl_2,
            'lvl_3_statuses': lvl_3
        }

