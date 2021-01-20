import datetime
import random
import pandas as pd
import numpy as np
from joblib import load
import os
import statistics
from datetime import timedelta

# Generate relative path
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../ml_models/outputs/murb_power_regression.joblib')

# Load Model
loaded_clf = load(filename)

# Fucntion Requires datetime object

def power_from_time(time, parameters):
    # Predict output power
    #time = time - timedelta(hours=8) #Convert to EST for data model
    data_time = {'hour':time.hour, 'month':time.month}
    data_averages = {'avgPowerSummer': float(parameters['avgPowerSummer']), 'avgPowerWinter': float(parameters['avgPowerWinter']), 'avgPowerSpring': float(parameters['avgPowerSpring']), 'avgPowerFall': float(parameters['avgPowerFall']), 'avgPower': float(parameters['avgPower'])}

    df_1 = pd.DataFrame(data_time, columns = ['hour','month'], index=[0])
    df_2 = pd.DataFrame(data_averages, columns = ['avgPowerSummer', 'avgPowerWinter', 'avgPowerSpring', 'avgPowerFall'], index=[0])

    df_2 = df_2.div(float(parameters['avgPower']))

    df = pd.concat([df_1, df_2], axis=1)

    
    predict_output_power = loaded_clf.predict(df)
    
    if time.weekday() < 5:
        return predict_output_power[0]*float(parameters['avgPower']) + predict_output_power[0]*float(parameters['avgPower'])*(-0.05) + random.uniform(-0.01*predict_output_power[0]*float(parameters['avgPower']),0.01*predict_output_power[0]*float(parameters['avgPower']))
    else:
        return predict_output_power[0]*float(parameters['avgPower']) + predict_output_power[0]*float(parameters['avgPower'])*0.025 + random.uniform(-0.01*predict_output_power[0]*float(parameters['avgPower']),0.01*predict_output_power[0]*float(parameters['avgPower']))
