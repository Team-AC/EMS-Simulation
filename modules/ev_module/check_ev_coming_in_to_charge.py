import random
from random import randrange, gauss
from datetime import time, datetime


def check_ev_coming_in_to_charge(ev_start_time, parameter_dict):
    ev_start_time_hour = ev_start_time.hour
    chance_ev_wants_charge = random.uniform(0, 1) # this the chance that ev comes in and wants to charge
    probability_of_ev_entered = float(parameter_dict['percentageOfEv']) #Default Value

    if ev_start_time_hour >= 0 and ev_start_time_hour < 7: # 12am - 6am
        probability_of_ev_charging = 0.2
        if (chance_ev_wants_charge <= probability_of_ev_charging*probability_of_ev_entered):     
            ev_wanting_charge = True
            ev_battery_start_percentage = round(gauss(30,15)) # NEED TO CHANGE FOR BETTER ACCURACY
            print('ev wants it b/t 12am - 6am')
            return ev_wanting_charge, ev_battery_start_percentage

        else:
            ev_wanting_charge = False
            print('ev dont wants it b/t 12am - 6am')
            return ev_wanting_charge, None

    elif ev_start_time_hour >= 7 and ev_start_time_hour < 13: # 7a, - 12pm
        probability_of_ev_charging = 0.3
        if (chance_ev_wants_charge <= probability_of_ev_charging*probability_of_ev_entered):     
            ev_wanting_charge = True
            ev_battery_start_percentage = round(gauss(30,15))# NEED TO CHANGE FOR BETTER ACCURACY
            print('ev wants it b/t 7am - 12pm')
            return ev_wanting_charge, ev_battery_start_percentage

        else:
            ev_wanting_charge = False
            print('ev dont wants it b/t 7am - 12pm')
            return ev_wanting_charge, None
    elif ev_start_time_hour >= 13 and ev_start_time_hour < 20: # 1pm - 7 pm
        probability_of_ev_charging = 0.60
        if (chance_ev_wants_charge <= probability_of_ev_charging*probability_of_ev_entered):     
            ev_wanting_charge = True
            ev_battery_start_percentage = round(gauss(30,15)) # NEED TO CHANGE FOR BETTER ACCURACY
            print('ev wants it b/t 1pm - 7pm')
            return ev_wanting_charge, ev_battery_start_percentage

        else:
            ev_wanting_charge = False
            print('ev dont wants it b/t 1pm - 7pm')
            return ev_wanting_charge, None
    else:
        probability_of_ev_charging = 0.85
        if (chance_ev_wants_charge <= probability_of_ev_charging*probability_of_ev_entered):     
            ev_wanting_charge = True
            ev_battery_start_percentage = round(gauss(30,15)) # NEED TO CHANGE FOR BETTER ACCURACY
            print('ev wants it b/t 8pm - 12am')
            return ev_wanting_charge, ev_battery_start_percentage

        else:
            ev_wanting_charge = False
            print('ev dont wants it b/t 8pm - 12am')
            return ev_wanting_charge, None
