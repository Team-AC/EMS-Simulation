
def inflation_rate_calculation(principal, interest, financeParamaters):
    inflation_increase_list = []
    for year in range(int(financeParamaters['amountOfYears'])):
        total = float(principal)*float((1+interest)**float(year+1))
        inflation_increase_list.append(total)
    return inflation_increase_list
    

def ev_growth(initial, growthpercent, financeParamaters):
    ev_growth_list = []
    for year in range(int(financeParamaters['amountOfYears'])):
        new_growth = float(initial)*float((1+growthpercent)**float(year+1))
        ev_growth_list.append(new_growth)
    return ev_growth_list

def expected_battery_calculation(financeParamaters):
    expected_battery_size = int(financeParamaters['evSmallBatteryAverage'])*float(financeParamaters['evSmallBatteryProbability'])\
    + int(financeParamaters['evMediumBatteryAverage'])*float(financeParamaters['evMediumBatteryProbability'])\
    + int(financeParamaters['evLargeBatteryAverage'])*float(financeParamaters['evLargeBatteryProbability'])
    #print(expected_battery_size)
    return expected_battery_size

def ev_arrivals(financeParamaters):
    num_of_ev_per_year = []
    expected_battery_size = expected_battery_calculation(financeParamaters)
    ev_growth_charger = ev_growth(initial=float(financeParamaters['evArrivalsPerYear']), growthpercent=float(financeParamaters['evGrowthPerYear']), financeParamaters=financeParamaters)
    for year in range(int(financeParamaters['amountOfYears'])):
        arrival_expectation = float(ev_growth_charger[year])
        num_of_ev_per_year.append(arrival_expectation)
    return num_of_ev_per_year


def cost_per_charge(financeParamaters):
    cost_per = []
    average_charge_percentage = 0.6
    expected_battery_size = expected_battery_calculation(financeParamaters)
    charge_amount = expected_battery_size*average_charge_percentage
    charge_cost_per_kwh = inflation_rate_calculation(principal=float(financeParamaters['energyCost']), interest=0.02, financeParamaters=financeParamaters)

    for year in range(int(financeParamaters['amountOfYears'])):
        
        cost_level_2 = float(charge_cost_per_kwh[year])*float(charge_amount)

        cost_per.append(cost_level_2)

    return cost_per


def charger_cost_for_a_year(financeParamaters):
    level_3_charge = []
    level_2_charge = []
    num_of_ev_per_year = ev_arrivals(financeParamaters)
    cost_per = cost_per_charge(financeParamaters)
    for year in range(int(financeParamaters['amountOfYears'])):
        # level 2
        lvl_2_cost_for_year = float(financeParamaters['arrivalFlowPercentageLevel2'])*float(num_of_ev_per_year[year])*float(cost_per[year])
        lvl_3_cost_for_year = float(financeParamaters['arrivalFlowPercentageLevel3'])*float(num_of_ev_per_year[year])*float(cost_per[year])

        level_2_charge.append(lvl_2_cost_for_year)
        level_3_charge.append(lvl_3_cost_for_year)
    return level_2_charge,level_3_charge


def finance_init(sio):

    @sio.on('Generate Finance')
    def generate_finance(financeParamaters):
        return_level_2, return_level_3 = charger_cost_for_a_year(financeParamaters)
        list_future_projections = []
        
        for year in range(int(financeParamaters['amountOfYears'])):
            list_future_projections.append({
                'year': year,
                'lvl_2': return_level_2[year],
                'lvl_3': return_level_3[year]

            })

        return list_future_projections