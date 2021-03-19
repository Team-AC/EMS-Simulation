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

        def search(interval):
            for p in historic_data:
                if p['interval'] == interval:
                    return p
        
        list_predict = []

        for timestamp in list_timestamps:
            list_predict.append({
                'TimeStamp': timestamp,
                'Power': 0
            })

        past_month_dictionary = search('pastMonth')
        past_3_months_dictionary = search('past3Months')
        past_year_dictionary = search('pastYear')
        
        def get_value(listOfDicts, key):
            for subVal in listOfDicts:
                if key in subVal:
                    return subVal[key]

    

        #Aggregated Data Segments
        aggregated_data1 = historic_data[0]['aggregatedData']
        aggregated_data2 = historic_data[1]['aggregatedData']
        aggregated_data3 = historic_data[2]['aggregatedData']

        #Total Power Segments
        total_power_segment1 = [sub['TotalPower'] for sub in aggregated_data1]
        total_power_segment2 = [sub['TotalPower'] for sub in aggregated_data2]
        total_power_segment3 = [sub['TotalPower'] for sub in aggregated_data3]

        #EV Charger Type Segments
        charger_type1 = [sub['EvChargerType'] for sub in aggregated_data1]
        charger_type2 = [sub['EvChargerType'] for sub in aggregated_data2]
        charger_type3 = [sub['EvChargerType'] for sub in aggregated_data3]

        #Aggregated Amount Segments
        aggregated_amount_segment1 = [sub['AggregatedAmount'] for sub in aggregated_data1]
        aggregated_amount_segment2 = [sub['AggregatedAmount'] for sub in aggregated_data2]
        aggregated_amount_segment3 = [sub['AggregatedAmount'] for sub in aggregated_data3]

        #Timestamp Segments
        timestamp_segment_1 = [sub['TimeStamp'] for sub in aggregated_data1]
        timestamp_segment_2 = [sub['TimeStamp'] for sub in aggregated_data2]
        timestamp_segment_3 = [sub['TimeStamp'] for sub in aggregated_data3]

        #Hour Segments
        hour1 = []
        hour2 = []
        hour3 = []

        #Month Segments
        month1 = []
        month2 = []
        month3 = []

        #Hour Segment 1

        for value1 in timestamp_segment_1:
            append_time_parameters = dateutil.parser.parse(value1)
            hour1.append(append_time_parameters.day)
            month1.append(append_time_parameters.month)

        #Hour Segment 2

        for value2 in timestamp_segment_2:
            append_time_parameters2 = dateutil.parser.parse(value2)
            hour2.append(append_time_parameters2.day)
            month2.append(append_time_parameters2.month)

        #Hour Segment 3
        for value3 in timestamp_segment_3:
            append_time_parameters3 = dateutil.parser.parse(value3)
            hour3.append(append_time_parameters3.day)
            month3.append(append_time_parameters3.month)

        #Combine all the lists

        combined_list_segment_1 = month1 + hour1 + charger_type1 + aggregated_amount_segment1 + total_power_segment1
        combined_list_segment_2 = month2 + hour2 + charger_type2 + aggregated_amount_segment2 + total_power_segment2
        combined_list_segment_3 = month3 + hour3 + charger_type3 + aggregated_amount_segment3 + total_power_segment3

        #Machine Learning Aspect

        clf = RandomForestRegressor(n_estimators=500, oob_score=True, random_state=100) #Define Predictor
        
        df1_X = pd.DataFrame({'Month': month1, 'Hour': hour1, 'Charger Type': charger_type1})
        df1_y = pd.DataFrame({'Aggregated Amount': aggregated_amount_segment1, 'Total Power': total_power_segment1})

        df2_X = pd.DataFrame({'Month': month2, 'Hour': hour2, 'Charger Type': charger_type2})
        df2_y = pd.DataFrame({'Aggregated Amount': aggregated_amount_segment2, 'Total Power': total_power_segment2})

        df3_X = pd.DataFrame({'Month': month3, 'Hour': hour3, 'Charger Type': charger_type3})
        df3_y = pd.DataFrame({'Aggregated Amount': aggregated_amount_segment3, 'Total Power': total_power_segment3})

        test_hour= []
        test_month = []

        for value in list_timestamps:
            time1 = dateutil.parser.parse(value)
            test_hour.append(time1.hour)
            test_month.append(time1.month)

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


        #Create input dataframes
        df_input_lvl2 = pd.DataFrame({'Month': test_month, 'Hour': test_hour, 'Charger Type': ev_charger_type_input_lvl2})
        df_input_lvl3 = pd.DataFrame({'Month': test_month, 'Hour': test_hour, 'Charger Type': ev_charger_type_input_lvl3})

        clf.fit(df1_X, df1_y)
        clf.predict(df1_X)
        output1 = clf.predict(df_input_lvl2)
        output11 = clf.predict(df_input_lvl3)

        clf.fit(df2_X, df2_y)
        clf.predict(df2_X)
        output2 = clf.predict(df_input_lvl2)
        output22 = clf.predict(df_input_lvl3)

        clf.fit(df3_X, df3_y)
        clf.predict(df3_X)
        output3 = clf.predict(df_input_lvl2)
        output33 = clf.predict(df_input_lvl3)
        final_output = (1/3)*(output11 + output22 + output33)

        print(output22)
        class NumpyArrayEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return json.JSONEncoder.default(self, obj)

        encodedOutput = json.dumps(final_output, cls=NumpyArrayEncoder)
        

        return {'y1': encodedOutput}

