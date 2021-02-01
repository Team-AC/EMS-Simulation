import random

level_3_charge = {}
level_2_charge = {}
numofevperyear = {}
cost_per = {}
amount_of_years = 10
arrival_flow_percentage_level_2 = 0.25
arrival_flow_percentage_level_3 = 0.75


def inflation_rate_calculation(principal, interest):
    inflation_increase_dict = {}
    for year in range(amount_of_years):
        total = float(principal)*float((1+interest)**float(year+1))
        inflation_increase_dict.update({year:total})
    return inflation_increase_dict
    

def ev_growth(initial, growthpercent):
    ev_growth_dict = {}
    for year in range(amount_of_years):
        newgrowth = float(initial)*float((1+growthpercent)**float(year+1))
        ev_growth_dict.update({year:newgrowth})
    return ev_growth_dict

def ev_arrivals(financeParamaters):
    lvl_2_used = ev_growth(initial = 3000, growthpercent = 0.01)
    lvl_3_used = ev_growth(initial = 3000, growthpercent = 0.01)
    for year in range(amount_of_years):
        lvl_2_small_ev = arrival_flow_percentage_level_2*float(lvl_2_used[year])*float(financeParamaters['evSmallBatteryProbability'])
        lvl_2_med_ev = arrival_flow_percentage_level_2*float(lvl_2_used[year])*float(financeParamaters['evMediumBatteryProbability'])
        lvl_2_large_ev = arrival_flow_percentage_level_2*float(lvl_2_used[year])*float(financeParamaters['evLargeBatteryProbability'])

        lvl_3_small_ev = arrival_flow_percentage_level_3*float(lvl_3_used[year])*float(financeParamaters['evSmallBatteryProbability'])
        lvl_3_med_ev = arrival_flow_percentage_level_3*float(lvl_3_used[year])*float(financeParamaters['evMediumBatteryProbability'])
        lvl_3_large_ev = arrival_flow_percentage_level_3*float(lvl_3_used[year])*float(financeParamaters['evLargeBatteryProbability'])

        numofevperyear.update({year: [lvl_2_small_ev, lvl_2_med_ev, lvl_2_large_ev, lvl_3_small_ev, lvl_3_med_ev, lvl_3_large_ev]})
    return numofevperyear

def chargetime(financeParamaters):
    average_charge_percentage = 0.6
    charge_amount_small = int(financeParamaters['evSmallBatteryAverage'])*average_charge_percentage
    charge_amount_med = int(financeParamaters['evMediumBatteryAverage'])*average_charge_percentage
    charge_amount_large = int(financeParamaters['evLargeBatteryAverage'])*average_charge_percentage
    lvl_2_charge_time = {
        'chargetimesmall_lvl2' : charge_amount_small/int(financeParamaters['evLevel2ChargeRate']),
        'chargetimemed_lvl2' : charge_amount_med/int(financeParamaters['evLevel2ChargeRate']),
        'chargetimelarge_lvl2' : charge_amount_large/int(financeParamaters['evLevel2ChargeRate'])
    }
    lvl_3_charge_time = {
        'chargetimesmall_lvl3' : charge_amount_small/int(financeParamaters['evLevel3ChargeRate']),
        'chargetimemed_lvl3' : charge_amount_med/int(financeParamaters['evLevel3ChargeRate']),
        'chargetimelarge_lvl3' : charge_amount_large/int(financeParamaters['evLevel3ChargeRate'])
    }
    return lvl_2_charge_time, lvl_3_charge_time


def cost_per_charge(financeParamaters):
    lvl_2_charge_time, lvl_3_charge_time = chargetime(financeParamaters)
    lvl_2_charge_cost_per_hour = inflation_rate_calculation(principal = 2, interest= 0.02)
    lvl_3_charge_cost_per_hour = inflation_rate_calculation(principal = 15, interest= 0.02)
    for year in range(amount_of_years):
        cost_level_2_small = float(lvl_2_charge_cost_per_hour[year])*float(lvl_2_charge_time['chargetimesmall_lvl2'])
        cost_level_2_medium = float(lvl_2_charge_cost_per_hour[year])*float(lvl_2_charge_time['chargetimemed_lvl2'])
        cost_level_2_large = float(lvl_2_charge_cost_per_hour[year])*float(lvl_2_charge_time['chargetimelarge_lvl2'])

        cost_level_3_small = float(lvl_3_charge_cost_per_hour[year])*float(lvl_3_charge_time['chargetimesmall_lvl3'])
        cost_level_3_medium = float(lvl_3_charge_cost_per_hour[year])*float(lvl_3_charge_time['chargetimemed_lvl3'])
        cost_level_3_large = float(lvl_3_charge_cost_per_hour[year])*float(lvl_3_charge_time['chargetimelarge_lvl3'])
        cost_per.update({year: [cost_level_2_small, cost_level_2_medium, cost_level_2_large, cost_level_3_small, cost_level_3_medium, cost_level_3_large]})

    return cost_per


def charger_cost_for_a_year(financeParamaters):
    numofevperyear = ev_arrivals(financeParamaters)
    cost_per = cost_per_charge(financeParamaters)
    for year in range(amount_of_years):
        # level 2
        lvl_2_small_for_year = float(numofevperyear[year][0])*float(cost_per[year][0])
        lvl_2_med_for_year = float(numofevperyear[year][1])*float(cost_per[year][1])
        lvl_2_large_for_year = float(numofevperyear[year][2])*float(cost_per[year][2])
        # level 3
        lvl_3_small_for_year =  float(numofevperyear[year][3])*float(cost_per[year][3])
        lvl_3_med_for_year = float(numofevperyear[year][4])*float(cost_per[year][4])
        lvl_3_large_for_year = float(numofevperyear[year][5])*float(cost_per[year][5])

        # combined 
        lvl_2_combined_cost = lvl_2_small_for_year + lvl_2_med_for_year + lvl_2_large_for_year
        lvl_3_combined_cost = lvl_3_small_for_year + lvl_3_med_for_year + lvl_3_large_for_year

        level_2_charge.update({year:[lvl_2_small_for_year,lvl_2_med_for_year,lvl_2_large_for_year,lvl_2_combined_cost]})
        level_3_charge.update({year:[lvl_3_small_for_year, lvl_3_med_for_year, lvl_3_large_for_year,lvl_3_combined_cost]})
    return level_2_charge, level_3_charge


def finance_init(sio):

    @sio.on('Generate Finance')
    def generate_finance(financeParamaters):
        return_level_2, return_level_3 = charger_cost_for_a_year(financeParamaters)
        list_future_projections = []
        
        for year in range(amount_of_years):
            list_future_projections.append({
                'year': year,
                'lvl_2_small': return_level_2[year][0],
                'lvl_2_medium': return_level_2[year][1],
                'lvl_2_large': return_level_2[year][2],
                'lvl_3_small': return_level_3[year][0],
                'lvl_3_medium': return_level_3[year][1],
                'lvl_3_large': return_level_3[year][2],
                'lvl_3_combined_cost': return_level_3[year][3],
                'lvl_2_combined_cost': return_level_2[year][3]

            })

        return list_future_projections