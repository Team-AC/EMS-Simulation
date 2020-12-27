from datetime import datetime
from threading import Timer

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
    ev_entered = True
    charge_time = 15
    power = 30

    if (ev_entered):
        start_charging(charge_time, power)

def ev_simulation_init(sio_passed_in):
    global sio
    sio = sio_passed_in

    sio.sleep(1)

    def real_time_data():
        check_ev()
        Timer(30, check_ev).start()

    real_time_data()
