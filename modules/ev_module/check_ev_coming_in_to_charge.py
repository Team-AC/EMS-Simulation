import random
from random import randrange



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
        return ev_wanting_charge, ev_battery_start_percentage 
        #check_ev_charger(ev_wanting_charge, ev_battery_start_percentage)
    else:
        ev_wanting_charge = False
        print('ev dont wants it')
        return ev_wanting_charge, None
