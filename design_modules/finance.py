
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


def linear_growth_rate_calculator(present, future, financeParamaters):
    linear_growth_list = []
    for year in range(int(financeParamaters['amountOfYears'])):
        difference = (float(future)-float(present))/financeParamaters['amountOfYears']
        amount_for_that_year = float(present) + difference*float(year+1)
        linear_growth_list.append(amount_for_that_year)
    return linear_growth_list


def ev_arrivals(financeParamaters):
    ev_arrival = linear_growth_rate_calculator(present=financeParamaters['present']['evArrivalsPerYear'],\
    future=financeParamaters['future']['evArrivalsPerYear'], financeParamaters=financeParamaters)

    return ev_arrival


def cost_per_charge(financeParamaters):
    cost_per = []
    
    average_charge_percentage = linear_growth_rate_calculator(present=financeParamaters['present']['averageChargePercentage'],\
    future=financeParamaters['future']['averageChargePercentage'], financeParamaters=financeParamaters)

    battery_size = linear_growth_rate_calculator(present=financeParamaters['present']['averageBatterySize'],\
    future=financeParamaters['future']['averageBatterySize'], financeParamaters=financeParamaters)
 
    charge_cost_per_kwh = inflation_rate_calculation(principal=float(financeParamaters['present']['energyCost']), interest=float(financeParamaters['inflationRate']),\
    financeParamaters=financeParamaters)

    for year in range(int(financeParamaters['amountOfYears'])):
        charge_amount = average_charge_percentage[year]*battery_size[year]
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


def network_cost(financeParamaters):
    network_cost_per_year = linear_growth_rate_calculator(present=financeParamaters['present']['networkCost'], future=financeParamaters['future']['networkCost'], \
    financeParamaters=financeParamaters)
    return network_cost_per_year


def maintenance_cost(financeParamaters):

    maintenance_cost_per_year_lvl_2 = linear_growth_rate_calculator(present=financeParamaters['present']['maintenanceLevel2'], future=financeParamaters['future']['maintenanceLevel2'], \
    financeParamaters=financeParamaters)
    maintenance_cost_per_year_lvl_3 = linear_growth_rate_calculator(present=financeParamaters['present']['maintenanceLevel3'], future=financeParamaters['future']['maintenanceLevel3'], \
    financeParamaters=financeParamaters)

    return maintenance_cost_per_year_lvl_2, maintenance_cost_per_year_lvl_3

def finance_init(sio):

    @sio.on('Generate Finance')
    def generate_finance(financeParamaters):
        return_level_2, return_level_3 = charger_cost_for_a_year(financeParamaters)
        return_network_cost = network_cost(financeParamaters)
        return_maintenance_cost_lvl_2, return_maintenance_cost_lvl_3 = maintenance_cost(financeParamaters)
        return_ev_arrival = ev_arrivals(financeParamaters)
        list_future_projections = []
        
        for year in range(int(financeParamaters['amountOfYears'])):
            list_future_projections.append({
                'year': year,
                'network_cost': return_network_cost[year],
                'ev_arrival': return_ev_arrival[year],
                'lvl_2_maintenance_cost': return_maintenance_cost_lvl_2[year],
                'lvl_3_maintenance_cost': return_maintenance_cost_lvl_3[year],
                'lvl_2': return_level_2[year],
                'lvl_3': return_level_3[year]

            })

        return list_future_projections