import datetime
import random

mean = 0
variance = 10


week_number = datetime.datetime.today().weekday()


hour_dict = {
    "0": 232,
    "1": 219,
    "2": 205,
    "3": 205,
    "4": 203,
    "5": 200,
    "6": 222,
    "7": 252,
    "8": 266,
    "9": 271,
    "10": 279,
    "11": 290,
    "12": 298,
    "13": 298,
    "14": 291,
    "15": 297,
    "16": 302,
    "17": 325,
    "18": 352,
    "19": 354,
    "20": 340,
    "21": 324,
    "22": 302,
    "23": 262
}

month_dict = {
    "1": 83.5,
    "2": 88.5,
    "3": 60.5,
    "4": 36.04,
    "5": 48.5,
    "6": 112.03,
    "7": 153.5,
    "8": 133.5,
    "9": 114.3,
    "10": 75.5,
    "11": 72,
    "12": 82,
}

# Fucntion Requires datetime object


def power_from_time(time, parameters):

    M = month_dict[str(time.month)]

    H = hour_dict[str(time.hour)]

    if week_number < 5:
        return M + H + 20*random.random() - 20*random.random()
    else:
        return M + H + 20*random.random() - 20*random.random() + 15
