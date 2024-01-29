import numpy as np
import matplotlib.pyplot as plt


def pf_setup():
    # Import the ProFAST module
    import ProFAST

    # Create an ProFAST instance
    pf = ProFAST.ProFAST() 

    #
    # Set the parameters
    #

    # Define general inflation rate
    gen_inflation = 0.019

    #   Sales specification
    pf.set_params('commodity',{"name":'Hydrogen',"unit":"kg","initial price":4,"escalation":gen_inflation}) # Define the primary commodity
    pf.set_params('analysis start year',2025)
    pf.set_params('operating life',30) # Years of production
    pf.set_params('installation months',20) # Months of installation (no production)
    pf.set_params('demand rampup',2) # Years of ramp up (linear)
    pf.set_params('long term utilization',0.9) # The utilization or capacity factor of the plant, relative to the nameplate capacity

    # Installation information:
    pf.set_params('capacity',50000) #units/day # Nameplate capacity
    pf.set_params('installation cost',{"value":0,"depr type":"Straight line","depr period":5,"depreciable":False}) # Can be separated from capital items
    pf.set_params('non depr assets',10000) # Such as land
    pf.set_params('end of proj sale non depr assets',10000*(1+gen_inflation)**30) # Sale of land at project end
    pf.set_params('maintenance',{"value":5000,"escalation":gen_inflation}) # Annual maintenance cost

    #   Incentives specification
    pf.set_params('one time cap inct',{"value":250000,"depr type":"MACRS","depr period":5,"depreciable":False}) # Such as a capital grant, cost share, or investment tax credit 
    pf.set_params('annual operating incentive',{"value":1000,"decay":0,"sunset years":6,"taxable":True}) # Annual incentive (treated as income)
    pf.set_params('incidental revenue',{"value":500,"escalation":gen_inflation}) # Such as coffee sales

    #   Take or pay specification
    pf.set_params('TOPC',{"unit price":1,"decay":0.01,"support utilization":0.6,"sunset years":3}) # Underutilization support

    #   Other operating expenses
    pf.set_params('credit card fees',0.025) # Fraction of sales revenue
    pf.set_params('sales tax',0.023) # Fraction of sales revenue
    # pf.set_params('road tax',{"value":0,"escalation":0}) # Cost per unit of commodity ($/kg)
    pf.set_params('labor',{"value":20*40*52,"rate":20,"escalation":gen_inflation}) # 20 workers at 40hrs a week for 20$/hr
    pf.set_params('license and permit',{'value':2000,'escalation':gen_inflation}) # $/yr for licensing and permitting 
    pf.set_params('rent',{'value':50000,'escalation':gen_inflation}) # $/yr, for example for equipment
    pf.set_params('property tax and insurance',0.009) # Fraction of plant property and equipment
    pf.set_params('admin expense',0.005) # Fraction of sales revenue

    #   Financing information
    pf.set_params('total income tax rate',0.2574) # Combined tax rate
    pf.set_params('capital gains tax rate',0.15) # Only for any gains made on non depreciable assets
    pf.set_params('sell undepreciated cap',True)
    pf.set_params('tax losses monetized',True) # Offset coupled business tax liabilities
    pf.set_params('tax loss carry forward years',0) # If tax losses are carried forward
    pf.set_params('general inflation rate',gen_inflation) 
    pf.set_params('leverage after tax nominal discount rate',0.08) # Discount rate, and expected financial performance
    pf.set_params('debt equity ratio of initial financing',1.5) # D2E ratio at start
    pf.set_params('debt type','Revolving debt') # Bond/Revolving debt or one time loan
    pf.set_params('loan period if used',0) # Only for one time loan
    pf.set_params('debt interest rate',0.037) # Interest rate for loan
    pf.set_params('cash onhand',1) # Number of month of monthly expenses in liquidity


    #
    # Set the feedstocks
    #
    pf.add_feedstock(name='Water',usage=3.78,unit='gal',cost=0.005,escalation=gen_inflation) #3.78gal/kg H2
    pf.add_feedstock(name='Electricity (industrial)',usage=55.5,unit='kWh',cost=0.15,escalation=gen_inflation)

    # You can also use dictionaries and list to set the usages and costs
    years = list(map(str,range(2025-1,2025+30+2)))
    elec_usage = np.linspace(55.5,65,len(years))
    elec_usage_dict = dict(zip(years,elec_usage))
    elec_cost_dict = dict(zip(years, [0.15,0.14,0.2,0.75] ))
    pf.add_feedstock(name='Electricity (industrial) dict',usage=elec_usage_dict,unit='kWh',cost=0.15,escalation=gen_inflation)
    pf.remove_feedstock(name='Electricity (industrial) dict')

    # AEO feedstocks (Name and Cost must be valid values from AEO list)
    pf.edit_feedstock(name='Electricity (industrial)',value={'cost':'Mountain'})
    # AEO feedstocks can be modified for sensitivity analysis
    pf.edit_feedstock(name='Electricity (industrial)',value={'usage':55.5,'cost':'1.1X Mountain'})

    #
    # Set the coproducts
    #
    pf.add_coproduct(name='Oxygen',usage=7,unit='mol',cost=0.01,escalation=gen_inflation) 
    pf.edit_coproduct(name='Oxygen',value={'usage':7})


    #
    # Set the capital items
    #
    dol_per_kw = 500
    kW = 50000/24*55.5
    pf.add_capital_item(name='PEM Stack',cost=kW*dol_per_kw,depr_type='MACRS',depr_period=7,refurb=[0,0,0,0,0,0,0.15]*4) # Refurb 15% every 7 years
    pf.add_capital_item(name='BOP',cost=1000000,depr_type='MACRS',depr_period=7,refurb=[0])

    #
    # Set the fixed costs
    #
    pf.add_fixed_cost(name='Fixed costs',usage=1,unit='$',cost=3000000,escalation=gen_inflation)

    #
    # Set the incentives
    #
    pf.add_incentive(name='45V',value=3,decay=0,sunset_years=10,tax_credit=True)

    return pf



if __name__ == '__main__':
    pf = pf_setup()

    # Price setter mode
    NPV = pf.cash_flow()
    print(f'IRR: {pf.irr}')
    print(f'NPV: {NPV}')
    print("\n")

    # Price taker mode
    sol = pf.solve_price()
    price = sol['price']
    irr = sol['irr']
    ipp = sol['investor payback period']
    lco = sol['lco']
    print(f'First year price = {round(price,2)}')
    print(f'Levelized cost = {round(lco,2)}')
    print(f'IRR = {irr*100}%')
    print(f'Investor payback period = {round(ipp,2)}')

    # Plot cost breakdown
    pf.plot_costs()

    # Plot everything
    pf.plot_time_series()



    # What is the sensitivity to Electricity region?
    regions = ['US Average','East North Central','East South Central','Middle Atlantic','Mountain','New England','Pacific','South Atlantic','West North Central','West South Central']
    lcoh = []

    for region in regions:
        pf.edit_feedstock(name='Electricity (industrial)',value={'cost':region})
        sol = pf.solve_price()
        lcoh.append(sol['lco'])

    plt.bar(regions, lcoh)
    plt.xlabel("Regions")
    plt.ylabel("Levelized cost of H2 ($/kg)")
    plt.show()
    pass