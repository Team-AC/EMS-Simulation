import re
import sklearn
import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from joblib import dump, load
import os
import dateutil.parser
import json

def predict_ev_init(sio):

    @sio.on('Generate EV Prediction')
    def generate_ev_predict(historic_data, ev_predict_params, list_timestamps):

    
        # A search function is created to search for different time period keys
        
        def search(interval):
            for p in historic_data:
                if p['interval'] == interval:
                    return p
        
        
        past_month_dictionary = search('pastMonth')
        past_year_dictionary = search('pastYear')
        past_week_hourly_dictionary = search('pastWeekHourly')
        
        #Aggregated Data Segments
        past_month_aggregated_data = past_month_dictionary['aggregatedData']
        past_year_aggregated_data = past_year_dictionary['aggregatedData']
        past_week_hourly_aggregated_data = past_week_hourly_dictionary['aggregatedData']

        #Total Power Segments
        total_power_past_month = [sub['TotalPower'] for sub in past_month_aggregated_data]
        total_power_past_year = [sub['TotalPower'] for sub in past_year_aggregated_data]
        total_power_past_week_hourly = [sub['TotalPower'] for sub in past_week_hourly_aggregated_data]

        #EV Charger Type Segments
        charger_type_past_month = [sub['EvChargerType'] for sub in past_month_aggregated_data]
        charger_type_past_year = [sub['EvChargerType'] for sub in past_year_aggregated_data]
        charger_type_past_week_hourly = [sub['EvChargerType'] for sub in past_week_hourly_aggregated_data]

        #Aggregated Amount Segments
        aggregated_amount_past_month = [sub['AggregatedAmount'] for sub in past_month_aggregated_data]
        aggregated_amount_past_year = [sub['AggregatedAmount'] for sub in past_year_aggregated_data]
        aggregated_amount_past_week_hourly = [sub['AggregatedAmount'] for sub in past_week_hourly_aggregated_data]

        #Timestamp Segments
        timestamps_past_month = [sub['TimeStamp'] for sub in past_month_aggregated_data]
        timestamps_past_year = [sub['TimeStamp'] for sub in past_year_aggregated_data]
        timestamps_past_week_hourly = [sub['TimeStamp'] for sub in past_week_hourly_aggregated_data]

        #Empty lists segments of time (hours,days,months) as required

        #Day Segments
        day_past_month = []
        day_past_year = []
        day_past_week_hourly = []

        #Month Segments
        month_past_month = []
        month_past_year = []
        month_past_week_hourly = []

        #Hour Segments
        hour_past_month = []
        hour_past_year = []
        hour_past_week_hourly = []

        #Append segments of time (hours,days,months) past month

        for value1 in timestamps_past_month:
            append_time_parameters = dateutil.parser.parse(value1)
            day_past_month.append(append_time_parameters.day)
            month_past_month.append(append_time_parameters.month)
            hour_past_month.append(append_time_parameters.hour)

        #Append segments of time (hours,days,months) past year

        for value3 in timestamps_past_year:
            append_time_parameters3 = dateutil.parser.parse(value3)
            day_past_year.append(append_time_parameters3.day)
            month_past_year.append(append_time_parameters3.month)
            hour_past_year.append(append_time_parameters.hour)

        #Append segments of time (hours,days,months) past week hourly

        for value4 in timestamps_past_week_hourly:
            append_time_parameters3 = dateutil.parser.parse(value4)
            day_past_week_hourly.append(append_time_parameters3.day)
            month_past_week_hourly.append(append_time_parameters3.month)
            hour_past_week_hourly.append(append_time_parameters3.hour)

        #Machine Learning Aspect

        #Define Predictor

        clf = RandomForestRegressor(n_estimators=500, oob_score=True, random_state=100) 
        
        #Dataframe past month features

        df_past_month_X = pd.DataFrame({'Day': day_past_month, 'Charger Type': charger_type_past_month})
        df_past_month_y = pd.DataFrame({'Aggregated Amount': aggregated_amount_past_month, 'Total Power': total_power_past_month})

        #Dataframe past year features

        df_past_year_X = pd.DataFrame({'Month': month_past_year, 'Charger Type': charger_type_past_year})
        df_past_year_y = pd.DataFrame({'Aggregated Amount': aggregated_amount_past_year, 'Total Power': total_power_past_year})

        #Dataframe past week hourly features

        df_past_week_hourly_X = pd.DataFrame({'Hour': hour_past_week_hourly, 'Charger Type': charger_type_past_week_hourly})
        df_past_week_hourly_y = pd.DataFrame({'Aggregated Amount': aggregated_amount_past_week_hourly, 'Total Power': total_power_past_week_hourly})

        

        #Append segments of time (day,month,hour) for test parameters
        test_day= []
        test_month = []
        test_hour = []

        for value in list_timestamps:
            time_from_list = dateutil.parser.parse(value)
            test_day.append(time_from_list.day)
            test_month.append(time_from_list.month)
            test_hour.append(time_from_list.hour)

        
        #Define input charger type feature as a list for dataframe

        ev_charger_type_input_lvl2 = []
        length_list_of_timestamps = len(list_timestamps)
        i = 0

        while i < length_list_of_timestamps:
            charger = 2
            ev_charger_type_input_lvl2.append(charger)
            i = i + 1

        ev_charger_type_input_lvl3 = []
        k = 0
        
        while k < length_list_of_timestamps:
            ev_charger_type_input_lvl3.append(3)
            k = k + 1


        #Create input dataframes for lvl 2 and lvl 3 chargers respectively

        #For past month

        df_input_lvl2_past_month = pd.DataFrame({'Day': test_day, 'Charger Type': ev_charger_type_input_lvl2})
        df_input_lvl3_past_month = pd.DataFrame({'Day': test_day, 'Charger Type': ev_charger_type_input_lvl3})

        #For past year

        df_input_lvl2_past_year = pd.DataFrame({'Month': test_month, 'Charger Type': ev_charger_type_input_lvl2})
        df_input_lvl3_past_year = pd.DataFrame({'Month': test_month, 'Charger Type': ev_charger_type_input_lvl3})

        #For past week hourly

        df_input_lvl2_past_week_hourly = pd.DataFrame({'Hour': test_hour, 'Charger Type': ev_charger_type_input_lvl2})
        df_input_lvl3_past_week_hourly = pd.DataFrame({'Hour': test_hour, 'Charger Type': ev_charger_type_input_lvl3})

        #Prediction application for past month

        clf.fit(df_past_month_X, df_past_month_y)
        output_past_month_lvl2 = (clf.predict(df_input_lvl2_past_month))/24
        output_past_month_lvl3 = (clf.predict(df_input_lvl3_past_month))/24

        #Prediction application for past year

        clf.fit(df_past_year_X, df_past_year_y)
        output_past_year_lvl2 = (clf.predict(df_input_lvl2_past_year))/30.5
        output_past_year_lvl3 = (clf.predict(df_input_lvl3_past_year))/30.5

        #Prediction application for past week hourly

        clf.fit(df_past_week_hourly_X, df_past_week_hourly_y)

        output_past_week_hourly_lvl2 = clf.predict(df_input_lvl2_past_week_hourly)
        output_past_week_hourly_lvl3 = clf.predict(df_input_lvl3_past_week_hourly)

        #Weights for conservative, aggressive predictions, and neutral predictions 

        conservative_prediction = 0.6
        neutral_prediction = 0.3
        aggressive_prediction = 0.1

        #Add lvl2 and lvl3 charger outputs
      
        sum_of_lvl2 = (1/3)*(output_past_month_lvl2 + output_past_year_lvl2 + output_past_week_hourly_lvl2)
        sum_of_lvl3 = (1/3)*(output_past_month_lvl3 + output_past_year_lvl3 + output_past_week_hourly_lvl3)

        final_output = sum_of_lvl2 + sum_of_lvl3

        class NumpyArrayEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return json.JSONEncoder.default(self, obj)

        
        final_output1 = np.array(final_output.tolist())
        encodedOutput = json.dumps(final_output1, cls=NumpyArrayEncoder)
        return_list = json.loads(encodedOutput)
        
        f = encodedOutput.split()
       


        return return_list
        

