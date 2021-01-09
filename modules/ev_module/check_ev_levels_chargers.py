import numpy as np


def check_ev_level_2_charger(lvl_2):
    for i,in_use_or_not_in_use_level_2 in np.ndenumerate(lvl_2):
        if np.all(lvl_2):  
            full_ev_charger_level_2 = 1
            return 0,0,0,full_ev_charger_level_2
                 
        else:
            if in_use_or_not_in_use_level_2 == 0: #ev_charger is avavilable
                #print('lvl 2 charger is avaliable')
                ev_charger_level_2 = 2
                i = ''.join(map(str, i))
                ev_charger_level_2_num=int(i)
                full_ev_charger_level_2 = 0
                return ev_charger_level_2_num, ev_charger_level_2, in_use_or_not_in_use_level_2, full_ev_charger_level_2
        

def check_ev_level_3_charger(lvl_3):
    for i,in_use_or_not_in_use_level_3 in np.ndenumerate(lvl_3):
        if np.all(lvl_3):  
            full_ev_charger_level_3 = 1
            return 0,0,0,full_ev_charger_level_3
                 
        else:
            if in_use_or_not_in_use_level_3 == 0: #ev_charger is avavilable
                #print('lvl 3 charger is avaliable')
                ev_charger_level_3 = 3
                i = ''.join(map(str, i))
                ev_charger_level_3_num=int(i)
                full_ev_charger_level_3 = 0
                return ev_charger_level_3_num, ev_charger_level_3, in_use_or_not_in_use_level_3, full_ev_charger_level_3


