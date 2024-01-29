
def ProFAST_example():
    """This function gives an example file to run ProFAST
    :param None
    :return None
    """

#   ProFAST example
    import ProFAST
    import time

    #   Initialize ProFAST class
    pf = ProFAST.ProFAST('central_wind_electrolysis')
    # h2a = ProFAST.H2A_case('smr')

    #  Premade JSON input files can also be loaded using the load_json functionality
    pf.load_json('central_wind_electrolysis')

    #   Add a feed stock
    pf.add_feedstock(name='Residential electricity',usage=4,unit='kWh',cost=0.105427462,escalation=0.005)
    #   Add a capital item
    pf.add_capital_item(name='Compressor',cost=475286.1648,depr_type='MACRS',depr_period=5,refurb=[0.4401, 0.4401, 0.1011, 0.3871, 0.4686, 0.905 , 0.4024, 0.3172, 0.926 , 0.6936, 0.271 , 0     , 0     , 0     ])
    #   Add a fixed cost
    pf.add_fixed_cost(name='purity testing',usage=1,unit='$',cost=3483.816459,escalation=0.015246584)
    #   Add a coproduct
    pf.add_coproduct(name='Apples',usage=0.013394611,unit='bundles',cost=0.934823018,escalation=0.007012072)
    #   Add an incentive
    pf.add_incentive(name='LCFS',value=0.167811004,decay=0.00828,sunset_years=5,tax_credit=True)

    #   Remove a feedstock
    pf.remove_feedstock(name='Residential electricity')

    #   Edit a coproduct
    # pf.edit_coproduct('Apples',{'name':'Pears','usage':0.02})

    #   Dictionary (year,value) pairs can be used to set the usage and cost metrics
    years = list(map(str,range(1992,2100)))
    juice_costs = [1]*len(years)
    juice_cost_dict = dict(zip(years,juice_costs))
    juice_usage_dict = dict(zip(years,[10]*len(years)))
    pf.add_feedstock(name='juice',usage=juice_usage_dict,unit='barrels',cost=juice_cost_dict,escalation=2)

    #   Timer
    t1 = time.time()

    #  Solve for the break-price
    sol=pf.solve_price()

    #   Print out break even price
    price = sol['price']
    irr = sol['irr']
    ipp = sol['investor payback period']
    lco = sol['lco']
    print(f'First year price = {round(price,2)}')
    print(f'Levelized cost = {round(lco,2)}')
    print(f'IRR = {irr*100}%')
    print(f'Investor payback period = {round(ipp,2)}')

    #   Timer
    t2 = time.time()
    print(f'Time elapsed: {t2-t1}s')

    #   Load defaults from json file (the default inputs are loaded by default)
    pf.load_json('central_wind_electrolysis')

    #   Change sales tax
    # pf.set_params('sales tax',0.50)
    sol=pf.solve_price()

    #   Plot investor cash flow
    pf.plot_cashflow()

    #   Plot cost breakdown
    pf.plot_costs()

    #   Plot cost yearly breakdown
    pf.plot_costs_yearly()

    #   Plot cost yearly breakdown in plotly (interactive)
    pf.plot_costs_yearly2()

    #   Plot all time series in plotly (interactive)
    pf.plot_time_series()

    #   Solve for the break-price
    sol=pf.solve_price()
    price = sol['price']
    irr = sol['irr']
    ipp = sol['investor payback period']
    lco = sol['lco']
    print(f'First year price = {round(price,2)}')
    print(f'Levelized cost = {round(lco,2)}')
    print(f'IRR = {irr*100}%')
    print(f'Investor payback period = {round(ipp,2)}')


if __name__ == "__main__":
    ProFAST_example()