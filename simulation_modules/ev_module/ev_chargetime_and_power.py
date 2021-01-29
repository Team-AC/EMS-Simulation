from datetime import datetime
from threading import Timer
import random
from random import randrange, gauss
import numpy as np


def ev_chargetime_and_power(ev_wanting_charge,ev_battery_start_percentage, ev_charger_level, ev_charger_num, parameter_dict):
    chance_ev_battery_size = random.uniform(0, 1)
    ev_charger_lvl_2_rate = float(parameter_dict['evLevel2ChargeRate'])  #RATE for lvl 2 level two 7.7- 22 kw #Default Value
    ev_charger_lvl_3_rate = float(parameter_dict['evLevel3ChargeRate'])  #RATE for lvl 3 25 - 350 kw #Default Value
    ev_battery_small = round(gauss(float(parameter_dict['evSmallBatteryAverage']),10)) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
    ev_battery_med = round(gauss(float(parameter_dict['evMediumBatteryAverage']),10)) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE
    ev_battery_large = round(gauss(float(parameter_dict['evLargeBatteryAverage']),10)) #NEED TO FIND AVERAGE BATTERY CAPACITY FOR SIZE 
    ev_battery_small_probability = float(parameter_dict['evSmallBatteryProbability']) # setting a percentage as a decimal in total should equal 1.00
    ev_battery_med_probability = float(parameter_dict['evMediumBatteryProbability'])
    ev_battery_large_probability = float(parameter_dict['evLargeBatteryProbability'])

    if ev_wanting_charge == 1 and ev_charger_level == 2:
        if chance_ev_battery_size < ev_battery_small_probability: # 20% of EV's are small
            min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
            ev_battery_end_percentage = randrange(min_charge_percentage, 100, 1) # NEED TO CHANGE FOR BETTER ACCURACY
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_small
            charge_time = power/ev_charger_lvl_2_rate
            
            return charge_time, power, ev_charger_num, ev_charger_level
            
        elif ((chance_ev_battery_size >= ev_battery_small_probability) and (chance_ev_battery_size < (ev_battery_small_probability + ev_battery_med_probability))): # 60% of EV's are Medium size
            min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1) # this will be the leaving battery percentage 

           
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_med
            charge_time = power/ev_charger_lvl_2_rate
            
            return charge_time, power, ev_charger_num, ev_charger_level
        else:
            min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1) # this will be the leaving battery percentage 
            

            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_large
            charge_time = power/ev_charger_lvl_2_rate
            
            return charge_time, power, ev_charger_num, ev_charger_level       
    
    elif ev_wanting_charge == 1 and ev_charger_level == 3: # Level 3
       
        if chance_ev_battery_size < ev_battery_small_probability: # 20% of EV's are small
            min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1)
            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_small
            charge_time = power/ev_charger_lvl_3_rate

            return charge_time, power, ev_charger_num, ev_charger_level
            
        elif ((chance_ev_battery_size >= ev_battery_small_probability) and (chance_ev_battery_size < (ev_battery_small_probability + ev_battery_med_probability))): # 60% of EV's are Medium size
            min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1)

            
            #algo for power and time
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_med
            charge_time = power/ev_charger_lvl_3_rate

            return charge_time, power, ev_charger_num, ev_charger_level
            
        else:
            min_charge_percentage = ev_battery_start_percentage + round(gauss(10,2))
            ev_battery_end_percentage = randrange(min_charge_percentage,100,1)
            

            #algo for power and time
            
            power = ((ev_battery_end_percentage - ev_battery_start_percentage)/100)*ev_battery_large
            charge_time = power/ev_charger_lvl_3_rate

            return charge_time, power, ev_charger_num, ev_charger_level
 