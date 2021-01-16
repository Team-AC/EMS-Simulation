import random
from random import randrange, gauss
from datetime import time, datetime

def car_flow(parameter_dict):
    high_car_flow = 0.7
    med_car_flow = 0.2
    low_car_flow = 0.1
    car_coming_in = random.uniform(0,1)
    if parameter_dict['highCarFlow'] == "yes":
        if car_coming_in <= high_car_flow:
            print('High')
            return 1
        else:
            print('High')
            return 0
    elif parameter_dict['medCarFlow'] == "yes":
        if car_coming_in <= med_car_flow:
            print('Med')
            return 1
        else:
            print('Med')
            return 0
    elif parameter_dict['lowCarFlow'] == "yes":
        if car_coming_in <= low_car_flow:
            print('Low')
            return 1
        else:
            print('Low')
            return 0
    else:
        print('idk')
        return 1