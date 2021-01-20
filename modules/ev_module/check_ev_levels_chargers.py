import numpy as np
import random

def check_ev_level_2_charger(lvl_2):
    while True:
        ev_charger_level_2_num =  int(random.random() * len(lvl_2))
        if np.all(lvl_2):  
            full_ev_charger_level_2 = 1
            return 0,0,0,full_ev_charger_level_2
                 
        elif lvl_2[ev_charger_level_2_num] == 0: #ev_charger is avavilable
            #print('lvl 2 charger is avaliable')
            ev_charger_level_2 = 2
            full_ev_charger_level_2 = 0
            in_use_or_not_in_use_level_2 = 0
            return ev_charger_level_2_num, ev_charger_level_2, in_use_or_not_in_use_level_2, full_ev_charger_level_2

        

def check_ev_level_3_charger(lvl_3):
    while True:
        ev_charger_level_3_num = int(random.random() * len(lvl_3))
        if np.all(lvl_3):  
            full_ev_charger_level_3 = 1
            return 0,0,0,full_ev_charger_level_3
                 
        elif lvl_3[ev_charger_level_3_num] == 0: #ev_charger is avavilable
            #print('lvl 3 charger is avaliable')
            ev_charger_level_3 = 3
            full_ev_charger_level_3 = 0
            in_use_or_not_in_use_level_3 = 0
            return ev_charger_level_3_num, ev_charger_level_3, in_use_or_not_in_use_level_3, full_ev_charger_level_3




