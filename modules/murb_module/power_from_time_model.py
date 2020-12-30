import datetime
import random
import pandas as pd
import numpy as np
from joblib import load

# Load Model
loaded_clf =  load('ml_models\outputs\murb_power_regression.joblib')

# Define X_test


# Fucntion Requires datetime object

def power_from_time(time, parameters):
    # Predict output power

    data = {'hour':time.hour, 'month':time.month, 'avgPower': float(parameters['avgPower']), 'minPower': float(parameters['minPower']), 'maxPower': float(parameters['maxPower'])}
  
    df = pd.DataFrame(data, columns = ['hour','month','avgPower', 'minPower', 'maxPower'], index=[0])
    predict_output_power = loaded_clf.predict(df)
    return predict_output_power[0]
