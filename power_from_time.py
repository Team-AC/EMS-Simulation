import datetime
import random

hour_dict = {
  "0": 10,
  "1": 14,
  "2": 16,
  "4": 18,
  "5": 21,
  "6": 23,
  "7": 25,
  "8": 27,
  "9": 29,
  "10": 31,
  "11": 33,
  "12": 35,
  "13": 38,
  "14": 40,
  "15": 37,
  "16": 30,
  "17": 26,
  "18": 24,
  "19": 22,
  "20": 20,
  "21": 18,
  "22": 14,
  "23": 12
}

month_dict = {
  "1": 4,
  "2": 6,
  "3": 3,
  "4": 2,
  "5": 8,
  "6": 9,
  "7": 11,
  "8": 13,
  "9": 6,
  "10": 4,
  "11": 5,
  "12": 3,
}

def power_from_time(time):  

  M = month_dict[str(time.month)]  

  H = hour_dict[str(time.hour)]
  return M + H + random.random()
