
def finance_init(sio):

    @sio.on('Generate Finance')
    def generate_finance(financeParamaters):

        list_future_projections = []

        for year in range(25):
            list_future_projections.append({
                'year': year,
                'some_other_data': 3
            })

        return list_future_projections