from datetime import timedelta, datetime, timezone
from threading import Timer
from simulation_modules.bess_module.bess import Bess
from simulation_modules.bess_module.energy_control import EnergyControl
from simulation_modules.ev_module.check_ev_coming_in_to_charge import check_ev_coming_in_to_charge
from simulation_modules.ev_module.logic_ev_charger_check import logic_ev_charger_check
import time


ev_charging_queue = []
dict_interval_hours = {
    "pastDay": 24,
    "pastWeek": 24*7,
    "pastMonth": 24*30,
    "pastYear": 24*365
}

#Real Time Data
def end_charging(charge_time, power, ev_charger_num, ev_charger_level, in_use, lvl_2, lvl_3):
    global historical_current_time

    in_use = 0
    if ev_charger_level != 0:

        

        if ev_charger_level == 2:
            lvl_2[int(ev_charger_num)] = in_use
            #print("lvl 2",lvl_2)
        else:
            lvl_3[int(ev_charger_num)] = in_use
            #print("lvl 3",lvl_3)
        #print("charginggit  done and it good to use again")
        
        
        ev_time_stamp = historical_current_time 
        
        sio.emit('New EV Power', {
            'TimeStamp': ev_time_stamp.isoformat(),
            'Power': power,
            'ChargeTime': charge_time,
            'EvChargerNumber': ev_charger_num,
            'EvChargerType': ev_charger_level
        })

#Real Time Data
def start_charging(charge_time, power, ev_charger_num, ev_charger_level, in_use, lvl_2, lvl_3):
    global ev_charging_queue
    energy_control.request_ev_charge(power, ev_charger_level)
    ev_charging_queue.append({
        "finish_charging_time": historical_current_time + timedelta(hours=charge_time),
        "arguments": (charge_time, power, ev_charger_num, ev_charger_level, in_use, lvl_2, lvl_3)
    })
    
def historical_charge_queue(ev_parameters_dict):
    global historical_current_time
    global historical_start_time
    global bess
    global sio

    print('sim start', historical_current_time.date())

    time_increment = timedelta(seconds=30)
    energy_control.clock_update(historical_current_time)
    energy_control.charge_bess()
    
    while (historical_current_time < datetime.now(timezone.utc)):
        sim_current_day = historical_current_time.date()

        ev_wanting_charge, ev_battery_start_percentage = check_ev_coming_in_to_charge(historical_current_time, ev_parameters_dict)
        charge_time, power, ev_charger_num, ev_charger_level, _, in_use = logic_ev_charger_check(ev_wanting_charge, ev_battery_start_percentage, historical_current_time, lvl_2, lvl_3, ev_parameters_dict)
        if in_use == 1:
            start_charging(charge_time, power, ev_charger_num, ev_charger_level, in_use, lvl_2, lvl_3)
        
        # Check the queue, and execute end charging for any evs that are done
        for ev in ev_charging_queue:
            if (historical_current_time > ev['finish_charging_time']):
                end_charging(*ev['arguments'])
            
                index = ev_charging_queue.index({"finish_charging_time": ev['finish_charging_time'],"arguments": ev['arguments']})
                ev_charging_queue.pop(index)
        
        historical_prev_time = historical_current_time
        historical_current_time += time_increment
        energy_control.clock_update(historical_current_time)
        
        # New day has started
        if (historical_prev_time.hour == 23) and (historical_current_time.hour == 0):
            sio.emit("Historical Data Pause", historical_current_time.isoformat())

            break
            
def historical_data(interval, ev_parameters_dict, bess_parameters_dict, sio_passed_in): #(paramter_dict, sio)
    global sio
    sio = sio_passed_in
    global lvl_2
    global lvl_3
    global historical_current_time
    global ev_charging_queue
    global historical_start_time
    global energy_control

    lvl_2 = [0 for x in range(int(ev_parameters_dict['numOfEvLevel2']))]
    lvl_3 = [0 for x in range(int(ev_parameters_dict['numOfEvLevel3']))]
    historical_start_time = datetime.now(timezone.utc) - timedelta(hours=dict_interval_hours[interval])

    historical_current_time = historical_start_time
    
    bess = Bess(bess_parameters_dict, sio, historical_start_time)
    energy_control = EnergyControl(bess, [], ev_parameters_dict, bess_parameters_dict ,sio,historical_start_time)


    # Start the sim
    historical_charge_queue(ev_parameters_dict)

    # Continue the Sim When Server Says
    @sio.on("Historical Data Continue")
    def bess_schedule_update(schedule):
        historical_charge_queue(ev_parameters_dict)

