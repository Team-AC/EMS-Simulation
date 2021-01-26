import random
from random import randrange, gauss
from datetime import time, datetime

def car_flow(parameter_dict):
    high_car_flow = 0.7
    med_car_flow = 0.3
    low_car_flow = 0.15
    car_coming_in = random.uniform(0,1)
    if parameter_dict['carFlow'] == "high":
        if car_coming_in <= high_car_flow:
             return True
        else:
            return False
    elif parameter_dict['carFlow'] == "medium":
        if car_coming_in <= med_car_flow:
            return True
        else:
            return False
    elif parameter_dict['carFlow'] == "low":
        if car_coming_in <= low_car_flow:
            return True
        else:
            return False
    else:
        return True