from datetime import datetime
from threading import Timer
import random
from random import randrange, gauss
import numpy as np


def ev_chargetime_and_power(ev_wanting_charge,ev_battery_start_percentage, ev_charger_level, ev_charger_num):
    probability_of_evbattery_small = 0.2 # MIGHT CHANGE FOR ACCURACY
    probability_of_evbattery_med = 0.3
    probability_of_evbattery_large = 0.5
    chance_ev_battery_size = random.uniform(0, 1)
    
    if ev_wanting_charge == 1 and ev_charger_level == 2:
        if chance_ev_battery_size < 0.2:
            min_charge_percentage = ev_battery_start_percentage + round(gauss(15,5))
            ev_battery_end_percentage = randrange(min_charge_percentage, 100, 1) # NEED TO CHANGE FOR BETTER ACCURACY
            ev_battery_small = randrange(17,49,1) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_2_rate = 7 #RATE for lvl 2
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_small
            charge_time = power/ev_charger_lvl_2_rate 
            
            return charge_time, power, ev_charger_num, ev_charger_level
            
        elif ((chance_ev_battery_size >= 0.2) and (chance_ev_battery_size < 0.5)):
            min_charge_percentage = ev_battery_start_percentage + round(gauss(15,5))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1) # this will be the leaving battery percentage 
            ev_battery_med = randrange(50,84,1) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_2_rate = 7 #RATE for lvl 2
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_med
            charge_time = power/ev_charger_lvl_2_rate
            
            return charge_time, power, ev_charger_num, ev_charger_level
        else:
            min_charge_percentage = ev_battery_start_percentage + round(gauss(15,5))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1) # this will be the leaving battery percentage 
            ev_battery_large = randrange(85,200,1) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_2_rate = 7 #RATE for lvl 2

            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_large
            charge_time = power/ev_charger_lvl_2_rate
            
            return charge_time, power, ev_charger_num, ev_charger_level       
    
    elif ev_wanting_charge == 1 and ev_charger_level == 3: # Level 3
       
        if chance_ev_battery_size < 0.2:
            min_charge_percentage = ev_battery_start_percentage + round(gauss(15,5))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1)
            ev_battery_small = randrange(17,49,1) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_3_rate = 50 #RATE for lvl 3
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_small
            charge_time = power/ev_charger_lvl_3_rate

            return charge_time, power, ev_charger_num, ev_charger_level
            
        elif ((chance_ev_battery_size >= 0.2) and (chance_ev_battery_size < 0.5)):
            min_charge_percentage = ev_battery_start_percentage + round(gauss(15,5))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1)
            ev_battery_med = randrange(50,84,1) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_3_rate = 50 #RATE for lvl 3
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_med
            charge_time = power/ev_charger_lvl_3_rate

            return charge_time, power, ev_charger_num, ev_charger_level
            
        else:
            min_charge_percentage = ev_battery_start_percentage + round(gauss(15,5))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1)
            ev_battery_large = randrange(85,200,1) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
            ev_charger_lvl_3_rate = 50 #RATE for lvl 3

            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_large
            charge_time = power/ev_charger_lvl_3_rate

            return charge_time, power, ev_charger_num, ev_charger_level
 