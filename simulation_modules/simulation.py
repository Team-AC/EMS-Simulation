from simulation_modules.murb_module.murb_simulation import murb_simulation_init
from simulation_modules.ev_module.ev_simulation import ev_simulation_init
from simulation_modules.bess_module.bess_simulation import bess_simulation_init


def simulation_init(sio):

    murb_simulation_init(sio)
    ev_simulation_init(sio)
    bess_simulation_init(sio)
