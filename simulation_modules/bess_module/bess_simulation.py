from simulation_modules.bess_module.bess import Bess

real_time_bess = None

def bess_simulation_init(sio):

    @sio.on("Bess Init")
    def bess_init(bess_parameters):
        global real_time_bess

        real_time_bess = Bess(bess_parameters)

    @sio.on("Bess Charge")
    def bess_charge(charge_amount=None):
        real_time_bess.start_charging(real_time_bess.charge_capacity)

