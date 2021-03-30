from datetime import datetime
from threading import Timer
import random
from random import randrange, gauss
import numpy as np


def ev_chargetime_and_power(ev_wanting_charge,ev_battery_start_percentage, ev_charger_level, ev_charger_num, parameter_dict):
    chance_ev_battery_size = random.uniform(0, 1)
    ev_charger_lvl_2_rate = float(parameter_dict['evLevel2ChargeRate'])  #RATE for lvl 2 level two 7.7- 22 kw #Default Value
    ev_charger_lvl_3_rate = float(parameter_dict['evLevel3ChargeRate'])  #RATE for lvl 3 25 - 350 kw #Default Value
    ev_average_battery = round(gauss(float(parameter_dict['evBatteryAverage']),20)) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE


    if ev_wanting_charge == 1 and ev_charger_level == 2:

        min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
        ev_battery_end_percentage = randrange(min_charge_percentage,100,1) # this will be the leaving battery percentage 
        

        #algo for power and time
        power = (ev_battery_end_percentage - ev_battery_start_percentage)/100*ev_average_battery
        charge_time = power/ev_charger_lvl_2_rate
        
        return charge_time, power, ev_charger_num, ev_charger_level       
    
    elif ev_wanting_charge == 1 and ev_charger_level == 3: # Level 3

        min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
        ev_battery_end_percentage = randrange(min_charge_percentage,100,1)
        

        #algo for power and time
        
        power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_average_battery
        charge_time = power/ev_charger_lvl_3_rate

        return charge_time, power, ev_charger_num, ev_charger_level
    else:
        return 0,0,0,0
 