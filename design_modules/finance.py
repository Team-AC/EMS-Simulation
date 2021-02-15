
def inflation_rate_calculation(principal, interest, financeParamaters):
    inflation_increase_list = []
    for year in range(int(financeParamaters['present']['amountOfYears'])):
        total = float(principal)*float((1+interest)**float(year+1))
        inflation_increase_list.append(total)
    return inflation_increase_list
    

def ev_growth(initial, growthpercent, financeParamaters):
    ev_growth_list = []
    for year in range(int(financeParamaters['present']['amountOfYears'])):
        new_growth = float(initial)*float((1+growthpercent)**float(year+1))
        ev_growth_list.append(new_growth)
    return ev_growth_list


def ev_arrivals(financeParamaters):
    num_of_ev_per_year = []
    growth_percent = ((financeParamaters['future']['evArrivalsPerYear']-financeParamaters['present']['evArrivalsPerYear'])/(financeParamaters['present']['evArrivalsPerYear']))\
    /financeParamaters['present']['amountOfYears']
    ev_growth_charger = ev_growth(initial=float(financeParamaters['present']['evArrivalsPerYear']), growthpercent=growth_percent,\
    financeParamaters=financeParamaters)
    for year in range(int(financeParamaters['present']['amountOfYears'])):
        arrival_expectation = float(ev_growth_charger[year])
        num_of_ev_per_year.append(arrival_expectation)
    return num_of_ev_per_year


def cost_per_charge(financeParamaters):
    cost_per = []
    average_charge_percentage = financeParamaters['present']['averageChargePercentage']
    charge_amount = financeParamaters['present']['averageBatterySize']*average_charge_percentage
    charge_cost_per_kwh = inflation_rate_calculation(principal=float(financeParamaters['present']['energyCost']), interest=float(financeParamaters['present']['inflationRate']),\
    financeParamaters=financeParamaters)

    for year in range(int(financeParamaters['present']['amountOfYears'])):
        cost_level_2 = float(charge_cost_per_kwh[year])*float(charge_amount)
        cost_per.append(cost_level_2)

    return cost_per


def charger_cost_for_a_year(financeParamaters):
    level_3_charge = []
    level_2_charge = []
    num_of_ev_per_year = ev_arrivals(financeParamaters)
    cost_per = cost_per_charge(financeParamaters)
    for year in range(int(financeParamaters['present']['amountOfYears'])):
        # level 2
        lvl_2_cost_for_year = float(financeParamaters['present']['arrivalFlowPercentageLevel2'])*float(num_of_ev_per_year[year])*float(cost_per[year])
        lvl_3_cost_for_year = float(financeParamaters['present']['arrivalFlowPercentageLevel3'])*float(num_of_ev_per_year[year])*float(cost_per[year])

        level_2_charge.append(lvl_2_cost_for_year)
        level_3_charge.append(lvl_3_cost_for_year)
    return level_2_charge,level_3_charge

"""
def initial_cost(financeParamaters):
    initial_cost_lvl_2 = int(financeParamaters['numOfEvLevel2'])*float(financeParamaters['installCostLevel2'])
    initial_cost_lvl_3 = int(financeParamaters['numOfEvLevel3'])*float(financeParamaters['installCostLevel3'])

    return initial_cost_lvl_2, initial_cost_lvl_3"""

def network_cost(financeParamaters):
    network_cost_per_year = inflation_rate_calculation(principal=float(financeParamaters['present']['networkCost']), interest=float(financeParamaters['present']['inflationRate']), financeParamaters=financeParamaters)

    return network_cost_per_year


def maintenance_cost(financeParamaters):

    maintenance_cost_per_year_lvl_2 = inflation_rate_calculation(principal=float(financeParamaters['present']['maintenanceLevel2']), interest=float(financeParamaters['present']['inflationRate']), financeParamaters=financeParamaters)
    maintenance_cost_per_year_lvl_3 = inflation_rate_calculation(principal=float(financeParamaters['present']['maintenanceLevel3']), interest=float(financeParamaters['present']['inflationRate']), financeParamaters=financeParamaters)

    return maintenance_cost_per_year_lvl_2, maintenance_cost_per_year_lvl_3

def finance_init(sio):

    @sio.on('Generate Finance')
    def generate_finance(financeParamaters):
        return_level_2, return_level_3 = charger_cost_for_a_year(financeParamaters)
        return_network_cost = network_cost(financeParamaters)
        return_maintenance_cost_lvl_2, return_maintenance_cost_lvl_3 = maintenance_cost(financeParamaters)

        list_future_projections = []
        
        for year in range(int(financeParamaters['present']['amountOfYears'])):
            list_future_projections.append({
                'year': year,
                'network_cost': return_network_cost[year],
                'lvl_2_maintenance_cost': return_maintenance_cost_lvl_2[year],
                'lvl_3_maintenance_cost': return_maintenance_cost_lvl_3[year],
                'lvl_2': return_level_2[year],
                'lvl_3': return_level_3[year]

            })

        return list_future_projections