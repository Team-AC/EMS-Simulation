from design_modules.costcalculators import charger_cost_for_a_year, network_cost, maintenance_cost, surge_calculator, cost_before_surge, installation_cost

def finance_init(sio):

    @sio.on('Generate Finance')
    def generate_finance(financeParamaters):

        installation_cost_level_2, installation_cost_level_3 = installation_cost(financeParamaters)

        return_lvl_2_surge = surge_calculator(arrivalflow=financeParamaters['arrivalFlowPercentageLevel2'], financeParamaters=financeParamaters)
        return_surge_lvl_3 = surge_calculator(arrivalflow=financeParamaters['arrivalFlowPercentageLevel3'], financeParamaters=financeParamaters)

        return_level_2_regular = cost_before_surge(arrivalflow=financeParamaters['arrivalFlowPercentageLevel2'], financeParamaters=financeParamaters)
        return_level_3_regular = cost_before_surge(arrivalflow=financeParamaters['arrivalFlowPercentageLevel3'], financeParamaters=financeParamaters)

        return_level_2, return_level_3 = charger_cost_for_a_year(financeParamaters)
        return_network_cost = network_cost(financeParamaters)
        return_maintenance_cost_lvl_2, return_maintenance_cost_lvl_3 = maintenance_cost(financeParamaters)
        list_future_projections = []

        for year in range(int(financeParamaters['amountOfYears'])):
            list_future_projections.append({
                'year': year,
                'network_cost': return_network_cost[year],
                'lvl_2_installation_cost': installation_cost_level_2[year],
                'lvl_3_installation_cost': installation_cost_level_3[year],
                'lvl_2_maintenance_cost': return_maintenance_cost_lvl_2[year],
                'lvl_3_maintenance_cost': return_maintenance_cost_lvl_3[year],
                'lvl_2_no_surge_cost': return_level_2[year],
                'lvl_3_no_surge_cost': return_level_3[year],
                'lvl_2_before_surge': return_level_2_regular[year],
                'lvl_3_before_surge': return_level_3_regular[year],
                'lvl_2_surge':return_lvl_2_surge[year],
                'lvl_3_surge':return_surge_lvl_3[year]
            })

        return list_future_projections