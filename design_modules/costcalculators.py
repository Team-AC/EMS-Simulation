from design_modules.calculation_functions import inflation_rate_calculation, linear_growth_rate_calculator

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
 
    charge_cost_per_kwh = inflation_rate_calculation(principal=float(financeParamaters['energyCost']), interest=float(financeParamaters['inflationRate']),\
    financeParamaters=financeParamaters)

    for year in range(int(financeParamaters['amountOfYears'])):
        charge_amount = average_charge_percentage[year]*battery_size[year]
        cost_level_2 = float(charge_cost_per_kwh[year])*float(charge_amount)
        cost_per.append(cost_level_2)

    return cost_per, average_charge_percentage, battery_size


def charger_cost_for_a_year(financeParamaters):
    level_3_charge = []
    level_2_charge = []
    num_of_ev_per_year = ev_arrivals(financeParamaters)
    cost_per, average_charge_percentage, battery_size = cost_per_charge(financeParamaters)
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

def surge_calculator(financeParamaters):
    # i assume that for a year the amount of arrivals is evenly distributed across 12 months 
    cost_per, average_charge_percentage, battery_size = cost_per_charge(financeParamaters)
    ev_arrival = ev_arrivals(financeParamaters)

    kwh_rate_past_threshold = inflation_rate_calculation(principal=float(financeParamaters['energyCostPastThreshold']), interest=float(financeParamaters['inflationRate']),\
    financeParamaters=financeParamaters)

    max_amount_kw_for_reg_rate = linear_growth_rate_calculator(present=financeParamaters['present']['kwCapRegularRate'], future=financeParamaters['future']['kwCapRegularRate'], \
    financeParamaters=financeParamaters)

    surge_calculator_list = []
    for year in range(int(financeParamaters['amountOfYears'])):
        total_charge_kw_for_year = average_charge_percentage[year]*battery_size[year]*ev_arrival[year]*financeParamaters['arrivalFlowPercentageLevel3']
        if total_charge_kw_for_year > max_amount_kw_for_reg_rate[year]:
            kw_used_past_threshold = total_charge_kw_for_year - max_amount_kw_for_reg_rate[year]
            surged_price_for_year = kw_used_past_threshold*kwh_rate_past_threshold[year]
            surge_calculator_list.append(surged_price_for_year)

    return surge_calculator_list