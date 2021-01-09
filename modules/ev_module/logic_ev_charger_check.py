import random
from modules.ev_module.ev_chargetime_and_power import ev_chargetime_and_power
from modules.ev_module.check_ev_levels_chargers import check_ev_level_2_charger, check_ev_level_3_charger

def logic_ev_charger_check(ev_wanting_charge, ev_battery_start_percentage, ev_start_time, lvl_2, lvl_3):
    ev_charger_level_2_num, ev_charger_level_2, in_use_or_not_in_use_level_2, full_ev_charger_level_2 = check_ev_level_2_charger(lvl_2)
    ev_charger_level_3_num, ev_charger_level_3, in_use_or_not_in_use_level_3, full_ev_charger_level_3 = check_ev_level_3_charger(lvl_3)
    probability_of_using_level_2_or_3 = random.uniform(0,1) # will change maybe
    
    if (ev_wanting_charge):
        if probability_of_using_level_2_or_3 < 0.5: # lvl 2
            if full_ev_charger_level_2 == 0:
                print('lvl 2 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_2,ev_charger_level_2_num)                
                in_use_or_not_in_use_level_2 = 1 #ev charger in use
                lvl_2[ev_charger_level_2_num] = in_use_or_not_in_use_level_2
                print(lvl_2)
               #logic_ev_charger_check_return = {"charge_time" : charge_time, "power" : power, "ev_charger_num" : ev_charger_num, "ev_charger_level" : ev_charger_level, "ev_start_time" : ev_start_time, "in_use_or_not_in_use_level_2" : in_use_or_not_in_use_level_2}
               #print(logic_ev_charger_check_return)
                return charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use_or_not_in_use_level_2
            elif full_ev_charger_level_3 == 0:
                print("full lvl 2 but gonna use level 3")
                print('lvl 3 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_3,ev_charger_level_3_num)
                in_use_or_not_in_use_level_3 = 1 #ev charger in use
                lvl_3[ev_charger_level_3_num] = in_use_or_not_in_use_level_3
                print(lvl_3)
                #logic_ev_charger_check_return = {"charge_time" : charge_time, "power" : power, "ev_charger_num" : ev_charger_num, "ev_charger_level" : ev_charger_level, ev_start_time : ev_start_time, "in_use_or_not_in_use_level_3" : in_use_or_not_in_use_level_3}
                #print(logic_ev_charger_check_return)
                return charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use_or_not_in_use_level_3
            else:
                print("all full")
                return 0,0,0,0,0,0
        else:
            if full_ev_charger_level_3 == 0:
                print('lvl 3 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_3,ev_charger_level_3_num)
                in_use_or_not_in_use_level_3 = 1 #ev charger in use
                lvl_3[ev_charger_level_3_num] = in_use_or_not_in_use_level_3
                print(lvl_3)
                #logic_ev_charger_check_return = {"charge_time" : charge_time, "power" : power, "ev_charger_num" : ev_charger_num, "ev_charger_level" : ev_charger_level, "ev_start_time" : ev_start_time, "in_use_or_not_in_use_level_3" : in_use_or_not_in_use_level_3}
                #print(logic_ev_charger_check_return)
                return charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use_or_not_in_use_level_3
            elif full_ev_charger_level_2 == 0:
                print("full lvl 3 but gonna use level 2")
                print('lvl 2 charger is avaliable')
                charge_time, power, ev_charger_num, ev_charger_level = ev_chargetime_and_power(ev_wanting_charge, ev_battery_start_percentage, ev_charger_level_2,ev_charger_level_2_num)                 
                in_use_or_not_in_use_level_2 = 1 #ev charger in use
                lvl_2[ev_charger_level_2_num] = in_use_or_not_in_use_level_2
                print(lvl_2)
                #logic_ev_charger_check_return = {"charge_time" : charge_time, "power" : power, "ev_charger_num" : ev_charger_num, "ev_charger_level" : ev_charger_level, "ev_start_time" : ev_start_time, "in_use_or_not_in_use_level_2" : in_use_or_not_in_use_level_2}
                #print(logic_ev_charger_check_return)
                return charge_time, power, ev_charger_num, ev_charger_level, ev_start_time, in_use_or_not_in_use_level_2
            else:
                print("all full")
                return 0,0,0,0,0,0
    else:
        return 0,0,0,0,0,0