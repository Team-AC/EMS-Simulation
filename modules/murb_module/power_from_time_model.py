import datetime
import random
import pandas as pd
import numpy as np
from joblib import load
import os

# Generate relative path
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../ml_models/outputs/murb_power_regression.joblib')

# Load Model
loaded_clf = load(filename)

# Fucntion Requires datetime object

def power_from_time(time, parameters):
    # Predict output power

    data = {'hour':time.hour, 'month':time.month, 'avgPower': float(parameters['avgPower']), 'minPower': float(parameters['minPower']), 'maxPower': float(parameters['maxPower'])}
  
    df = pd.DataFrame(data, columns = ['hour','month','avgPower', 'minPower', 'maxPower'], index=[0])
    predict_output_power = loaded_clf.predict(df)
    return predict_output_power[0]
