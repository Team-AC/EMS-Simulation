def inflation_rate_calculation(principal, interest, financeParamaters):
    inflation_increase_list = []
    for year in range(int(financeParamaters['amountOfYears'])):
        total = float(principal)*float((1+interest)**float(year+1))
        inflation_increase_list.append(total)
    return inflation_increase_list
    
    
def linear_growth_rate_calculator(present, future, financeParamaters):
    linear_growth_list = []
    for year in range(int(financeParamaters['amountOfYears'])):
        difference = (float(future)-float(present))/float(financeParamaters['amountOfYears'])
        amount_for_that_year = float(present) + difference*float(year+1)
        linear_growth_list.append(amount_for_that_year)
    return linear_growth_list
