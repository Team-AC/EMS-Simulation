from datetime import datetime
from threading import Timer
import random
from random import randrange
import numpy as np
from modules.ev_module.check_ev_coming_in_to_charge import check_ev_coming_in_to_charge
from modules.ev_module.ev_chargetime_and_power import ev_chargetime_and_power



def end_charging(charge_time, power, ev_charger_num, ev_charger_level):
    global sio
    global in_use_or_not_in_use_level_2
    global in_use_or_not_in_use_level_3
    in_use_or_not_in_use_level_2 = 0
    in_use_or_not_in_use_level_3 = 0
    if ev_charger_level == 2:
        lvl_2[ev_charger_num] = in_use_or_not_in_use_level_2
        print("lvl 2",lvl_2)
    else:
        lvl_3[ev_charger_num] = in_use_or_not_in_use_level_3
        print("lvl 3",lvl_3)
    print("charging done and it good to use again")
    
    sio.emit('New EV Power', {
        'TimeStamp': datetime.utcnow().isoformat(),
        'Power': power,
        'ChargeTime': charge_time,
    })


def start_charging(charge_time, power, ev_charger_num, ev_charger_level):
    charge_time_in_sec = charge_time*3600
    Timer(10, end_charging, (charge_time, power,ev_charger_num, ev_charger_level)).start()

def num_of_ev_chargers(num_ev_level_2,num_ev_level_3):
    global lvl_2
    global lvl_3
    lvl_2 = [0 for x in range(num_ev_level_2)]
    lvl_3 = [0 for x in range(num_ev_level_3)]


def check_ev_level_2_charger():
    global in_use_or_not_in_use_level_2
    for i,in_use_or_not_in_use_level_2 in np.ndenumerate(lvl_2):
        if in_use_or_not_in_use_level_2 == 0: #ev_charger is avavilable
           # print('lvl 2 charger is avaliable')
            ev_charger_level_2 = 2
            i = ''.join(map(str, i))
            ev_charger_level_2_num=int(i)
            full_ev_charger_level_2 = 0
            return ev_charger_level_2_num, ev_charger_level_2, in_use_or_not_in_use_level_2, full_ev_charger_level_2
        else:
            full_ev_charger_level_2 = 1
            return 0, 0, 0, full_ev_charger_level_2
        

def check_ev_level_3_charger():
    global in_use_or_not_in_use_level_3
    for i,in_use_or_not_in_use_level_3 in np.ndenumerate(lvl_3):
        if in_use_or_not_in_use_level_3 == 0: #ev_charger is avavilable
            #print('lvl 3 charger is avaliable')
            ev_charger_level_3 = 3
            i = ''.join(map(str, i))
            ev_charger_level_3_num=int(i)
            full_ev_charger_level_3 = 0
            return ev_charger_level_3_num, ev_charger_level_3, in_use_or_not_in_use_level_3, full_ev_charger_level_3
        else:
            full_ev_charger_level_3 = 1
            return 0,0,0,full_ev_charger_level_3


def check_ev_charger(ev_wanting_charge, ev_battery_start_percentage):
    global in_use_or_not_in_use_level_2
    global in_use_or_not_in_use_level_3
    probability_of_using_level_2_or_3 = random.uniform(0,1) # will change maybe
    if (ev_wanting_charge):
        ev_charger_level_2_num, ev_charger_level_2, in_use_or_not_in_use_level_2, full_ev_charger_level_2 = check_ev_level_2_charger()
        ev_charger_level_3_num, ev_charger_level_3, in_use_or_not_in_use_level_3, full_ev_charger_level_3 = check_ev_level_3_charger()
        if probability_of_using_level_2_or_3 < 0.5: # lvl 2
            if full_ev_charger_level_2 == 0:
                print('lvl 2 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_2,ev_charger_level_2_num) 
                start_charging(charge_time, power, ev_charger_num, ev_charger_level)                
                in_use_or_not_in_use_level_2 = 1 #ev charger in use
                lvl_2[ev_charger_level_2_num] = in_use_or_not_in_use_level_2
                print(lvl_2)
            elif full_ev_charger_level_3 == 0:
                print("full lvl 2 but gonna use level 3")
                print('lvl 3 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_3,ev_charger_level_3_num)
                start_charging(charge_time, power, ev_charger_num, ev_charger_level)
                in_use_or_not_in_use_level_3 = 1 #ev charger in use
                lvl_3[ev_charger_level_3_num] = in_use_or_not_in_use_level_3
                print(lvl_3)
            else:
                print("all full")
        else:
            if full_ev_charger_level_3 == 0:
                print('lvl 3 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_3,ev_charger_level_3_num)
                start_charging(charge_time, power, ev_charger_num, ev_charger_level)
                in_use_or_not_in_use_level_3 = 1 #ev charger in use
                lvl_3[ev_charger_level_3_num] = in_use_or_not_in_use_level_3
                print(lvl_3)
            elif full_ev_charger_level_2 == 0:
                print("full lvl 3 but gonna use level 2")
                print('lvl 2 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_2,ev_charger_level_2_num) 
                start_charging(charge_time, power, ev_charger_num, ev_charger_level)                
                in_use_or_not_in_use_level_2 = 1 #ev charger in use
                lvl_2[ev_charger_level_2_num] = in_use_or_not_in_use_level_2
                print(lvl_2)
            else:
                print("all full")


def ev_simulation_init(sio_passed_in):
    global sio
    sio = sio_passed_in

    sio.sleep(1)
    #num_of_ev_chargers(3,3)
    def real_time_data():
        ev_wanting_charge, ev_battery_start_percentage = check_ev_coming_in_to_charge()
        check_ev_charger(ev_wanting_charge, ev_battery_start_percentage)
        Timer(5, real_time_data).start()
    
    #real_time_data()
    
    @sio.on('Generate Ev')
    def generate_ev(paramters_dict):
        num_of_ev_chargers(int(paramters_dict["num_ev_level_2"]),int(paramters_dict["num_ev_level_3"]))
        real_time_data()