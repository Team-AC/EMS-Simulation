from design_modules.costcalculators import charger_cost_for_a_year, network_cost, maintenance_cost

def finance_init(sio):

    @sio.on('Generate Finance')
    def generate_finance(financeParamaters):
        return_level_2, return_level_3 = charger_cost_for_a_year(financeParamaters)
        return_network_cost = network_cost(financeParamaters)
        return_maintenance_cost_lvl_2, return_maintenance_cost_lvl_3 = maintenance_cost(financeParamaters)
        list_future_projections = []
        
        for year in range(int(financeParamaters['amountOfYears'])):
            list_future_projections.append({
                'year': year,
                'network_cost': return_network_cost[year],
                'lvl_2_maintenance_cost': return_maintenance_cost_lvl_2[year],
                'lvl_3_maintenance_cost': return_maintenance_cost_lvl_3[year],
                'lvl_2': return_level_2[year],
                'lvl_3': return_level_3[year]

            })

        return list_future_projections