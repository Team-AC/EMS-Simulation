from datetime import datetime
from threading import Timer
import random
from random import randrange
import numpy as np


def end_charging(charge_time, power, ev_charger_num, ev_charger_level):
    global sio
    global in_use_or_not_in_use
    in_use_or_not_in_use = 0
    if ev_charger_level == 2:
        lvl_2[ev_charger_num] = in_use_or_not_in_use
    else:
        lvl_3[ev_charger_num] = in_use_or_not_in_use
    print("charging done and it good to use again")
    print(ev_charger_num)
    print("lvl 2",lvl_2)
    print("lvl 3",lvl_3)
    sio.emit('New EV Power', {
        'TimeStamp': datetime.utcnow().isoformat(),
        'Power': power,
        'ChargeTime': charge_time,
    })


def start_charging(charge_time, power, ev_charger_num, ev_charger_level):
    charge_time_in_sec = charge_time*3600
    Timer(10, end_charging, (charge_time, power,ev_charger_num, ev_charger_level)).start()

def ev_chargetime_and_power(ev_wanting_charge,ev_battery_start_percentage, ev_charger_level, ev_charger_num):
    probability_of_evbattery_small = 0.2 # MIGHT CHANGE FOR ACCURACY
    probability_of_evbattery_med = 0.3
    probability_of_evbattery_large = 0.5
    chance_ev_battery_size = random.uniform(0, 1)
    
    if ev_wanting_charge == 1 and ev_charger_level == 2:
        if chance_ev_battery_size < 0.2:
            ev_battery_end_percentage = randrange(ev_battery_start_percentage, 100, 1) # NEED TO CHANGE FOR BETTER ACCURACY
            ev_battery_small = 10 #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_2_rate = 7 #RATE for lvl 2
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_small
            charge_time = power/ev_charger_lvl_2_rate
            start_charging(charge_time, power, ev_charger_num,ev_charger_level)   
        elif ((chance_ev_battery_size >= 0.2) and (chance_ev_battery_size < 0.5)):
            ev_battery_end_percentage = randrange(ev_battery_start_percentage,100,1) # this will be the leaving battery percentage 
            ev_battery_med = 50 #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_2_rate = 7 #RATE for lvl 2
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_med
            charge_time = power/ev_charger_lvl_2_rate
            start_charging(charge_time, power, ev_charger_num, ev_charger_level)
        else:
            ev_battery_end_percentage = randrange(ev_battery_start_percentage,100,1) # this will be the leaving battery percentage 
            ev_battery_large = 100 #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_2_rate = 7 #RATE for lvl 2

            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_large
            charge_time = power/ev_charger_lvl_2_rate
            start_charging(charge_time, power, ev_charger_num,ev_charger_level)          
    
    elif ev_wanting_charge == 1 and ev_charger_level == 3: # Level 3
       
        if chance_ev_battery_size < 0.2:
            ev_battery_end_percentage = randrange(ev_battery_start_percentage,100,1) # NEED TO CHANGE FOR BETTER ACCURACY
            ev_battery_small = 10 #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_3_rate = 50 #RATE for lvl 3
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_small
            charge_time = power/ev_charger_lvl_3_rate
            start_charging(charge_time, power,ev_charger_num,ev_charger_level)   
        elif ((chance_ev_battery_size >= 0.2) and (chance_ev_battery_size < 0.5)):
            ev_battery_end_percentage = randrange(ev_battery_start_percentage,100,1) # this will be the leaving battery percentage 
            ev_battery_med = 50 #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_3_rate = 50 #RATE for lvl 3
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_med
            charge_time = power/ev_charger_lvl_3_rate
            start_charging(charge_time, power,ev_charger_num,ev_charger_level)
        else:
            ev_battery_end_percentage = randrange(ev_battery_start_percentage,100,1) # this will be the leaving battery percentage 
            ev_battery_large = 100 #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_3_rate = 50 #RATE for lvl 3

            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_large
            charge_time = power/ev_charger_lvl_3_rate
            start_charging(charge_time, power,ev_charger_num, ev_charger_level)    
        

def num_of_ev_chargers(num_ev_level_2,num_ev_level_3):
    global lvl_2
    global lvl_3
    lvl_2 = [0 for x in range(num_ev_level_2)]
    lvl_3 = [0 for x in range(num_ev_level_3)]


def check_ev_charger(ev_wanting_charge, ev_battery_start_percentage):
    global in_use_or_not_in_use
    probability_of_using_level_2_or_3 = random.uniform(0,1) # will change maybe
    ev_charger_level = 0

    if probability_of_using_level_2_or_3 < 0.5: # lvl 2
        for i,in_use_or_not_in_use in np.ndenumerate(lvl_2):
            if in_use_or_not_in_use == 0: #ev_charger is avavilable
                print('lvl 2 charger is avaliable')
                ev_charger_level = 2
                i = ''.join(map(str, i))
                ev_charger_level_2_num=int(i)
                break
        ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level,ev_charger_level_2_num)
        in_use_or_not_in_use = 1 #ev charger in use
        print(ev_charger_level_2_num) 
        lvl_2[ev_charger_level_2_num] = in_use_or_not_in_use
        print("lvl2 ava",lvl_2)
    
    else: # lvl 3
        for i,in_use_or_not_in_use in np.ndenumerate(lvl_3):
            if in_use_or_not_in_use == 0: #ev_charger is avavilable
                print('lvl 3 charger is avaliable')
                ev_charger_level = 3
                i = ''.join(map(str, i))
                ev_charger_level_3_num=int(i)
                break
        #print(ev_charger_level_3_num) 
        ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level,ev_charger_level_3_num)
        in_use_or_not_in_use = 1 #ev charger in use
        lvl_3[ev_charger_level_3_num] = in_use_or_not_in_use
        print("lvl3 ava", lvl_3) 


def check_ev_coming_in_to_charge():
    # user inputs: number of chargers, 

    # ASSUMING ONE CHARGER RN

    probability_of_ev_entered = 0.5
    probability_of_ev_charging = 0.85
    chance_ev_wants_charge = random.uniform(0, 1)
    
    # this the chance that ev comes in and wants to charge
    if (chance_ev_wants_charge <= probability_of_ev_charging*probability_of_ev_entered):
        
        ev_wanting_charge = True
        ev_battery_start_percentage = randrange(0,40,1) # NEED TO CHANGE FOR BETTER ACCURACY
        print('ev wants it')
        check_ev_charger(ev_wanting_charge, ev_battery_start_percentage)
    else:
        
        ev_wanting_charge = False
        print('ev dont wants it')

def ev_simulation_init(sio_passed_in):
    global sio
    sio = sio_passed_in

    sio.sleep(1)
    #num_of_ev_chargers(3,3)
    def real_time_data():
        check_ev_coming_in_to_charge()
        Timer(5, real_time_data).start()
    
    #real_time_data()
    @sio.on('Generate Ev')
    def generate_ev(paramters_dict):
        num_of_ev_chargers(int(paramters_dict["num_ev_level_2"]),int(paramters_dict["num_ev_level_3"]))
        real_time_data()
    
