import random
from random import randrange, gauss
from datetime import time, datetime

def car_flow(parameter_dict):
    high_car_flow = 0.7
    med_car_flow = 0.2
    low_car_flow = 0.1
    proability_of_one_car = 0.85
    proability_of_more_car = 0.05
    car_coming_in = random.uniform(0,1)
    multiple_cars = random.uniform(0,1)
    if parameter_dict['highCarFlow'] == "yes":
        if car_coming_in <= high_car_flow:
            if multiple_cars <= proability_of_one_car:
                print('High one car')
                num_of_cars = 1
                return True, num_of_cars
            else:
                print('High bare tings')
                num_of_cars = abs(round(gauss(2,0.1)))
                return True, num_of_cars
        else:
            return False, 0
    elif parameter_dict['medCarFlow'] == "yes":
        if car_coming_in <= med_car_flow:
            print('Med')
            if multiple_cars <= proability_of_one_car:
                print('High one car')
                num_of_cars = 1
                return True, num_of_cars
            else:
                print('High bare tings')
                num_of_cars = abs(round(gauss(2,0.1)))
                return True, num_of_cars
        else:
            print('Med')
            return False, 0
    elif parameter_dict['lowCarFlow'] == "yes":
        if car_coming_in <= low_car_flow:
            if multiple_cars <= proability_of_one_car:
                print('High one car')
                num_of_cars = 1
                return True, num_of_cars
            else:
                print('High bare tings')
                num_of_cars = abs(round(gauss(2,0.1)))
                return True, num_of_cars
        else:
            print('Low')
            return False, 0
    else:
        print('idk')
        return True, 1