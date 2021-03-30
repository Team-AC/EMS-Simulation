from simulation_modules.bess_module.bess import Bess
from datetime import datetime, timedelta, timezone

bess = None

def bess_simulation_init(sio):

    @sio.on("Bess Init")
    def bess_init(bess_parameters):
        global bess

        bess = Bess(bess_parameters, sio, datetime.now(timezone.utc) - timedelta(hours=24))

    @sio.on("Bess Charge")
    def bess_charge(charge_amount):
        if (charge_amount == 'full'):
            bess.start_charging(bess.charge_capacity)
        elif (charge_amount == 'empty'):
            bess.start_charging(-bess.charge_capacity)
        else:
            bess.start_charging(float(charge_amount))

