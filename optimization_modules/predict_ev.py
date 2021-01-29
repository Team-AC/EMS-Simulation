
def predict_ev_init(sio):

    @sio.on('Generate EV Prediction')
    def generate_ev_predict(historic_data, ev_predict_params, list_timestamps):

        list_predict = []

        for timestamp in list_timestamps:
            list_predict.append({
                'TimeStamp': timestamp,
                'Power': 0
            })

        return historic_data

