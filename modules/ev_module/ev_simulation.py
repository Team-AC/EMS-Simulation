from datetime import datetime
from threading import Timer
import random

def end_charging(charge_time, power):
    global sio

    sio.emit('New EV Power', {
        'TimeStamp': datetime.utcnow().isoformat(),
        'Power': power,
        'ChargeTime': charge_time,
    })

def start_charging(charge_time, power):
    Timer(charge_time, end_charging, (charge_time, power)).start()

def check_ev():
    # user inputs: number of chargers,
    
    # ASSUMING ONE CHARGER RN
    
    # this the chance that ev comes in and wants to charge
    probability_of_ev_entered = 0.05
    probability_of_ev_charging = 0.85
    chance_ev_wants_charge = random.uniform(0, 1)

    if (chance_ev_wants_charge <= probability_of_ev_entered*probability_of_ev_charging):
        ev_wanting_charge = True
    else:
        ev_wanting_charge = False

    # ev chargers avalible (for assume only one charger for now) # what charger is avablie and go to
    # charger in use or not
    
    # ev charge time and power consumed (to figure out)
    # small/med/Large battery

    probability_of_evbattery_small = 0.2
    probability_of_evbattery_med = 0.3
    probability_of_evbattery_large = 0.5
    chance_ev_battery_size = random.uniform(0, 1)

    if (ev_wanting_charge):

        if (chance_ev_battery_size < 0.2):
            charge_time = 10 # algo for time 
            power = 5 # algo for power 
            start_charging(charge_time, power)
        elif  ((chance_ev_battery_size >= 0.2) and (chance_ev_battery_size < 0.5)):
            charge_time = 20
            power = 10
            start_charging(charge_time, power)
        else:
            charge_time = 30
            power = 15
            start_charging(charge_time, power)

def ev_simulation_init(sio_passed_in = None):
    global sio
    sio = sio_passed_in

    sio.sleep(1)

    def real_time_data():
        check_ev()
        Timer(30, check_ev).start()

    real_time_data()
