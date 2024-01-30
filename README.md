# ProFAST
The Production Financial Analysis Scenario Tool (ProFAST) is the python version of H2FAST. ProFAST provides a quick and convenient in-depth financial analysis for production systems and services based on Generally Accepted Accounting Principles (GAAP) methodology.

Please see https://www.nrel.gov/hydrogen/h2fast.html for the H2FAST excel model

<img src="https://www.nrel.gov/hydrogen/assets/images/h2fast-icon.png" alt="H2FAST Logo" style="width:200px;"/>

# NOTICE
[NOTICE.txt](NOTICE.txt)

Copyright © 2023 Alliance for Sustainable Energy, LLC
These data were produced by the Alliance for Sustainable Energy, LLC (Contractor) under Contract No. DE-AC36-08GO28308 with the U.S. Department of Energy (DOE). During the period of commercialization or such other time period specified by the DOE, the Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this data to reproduce, prepare derivative works, and perform publicly and display publicly, by or on behalf of the Government. Subsequent to that period the Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this data to reproduce, prepare derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so. The specific term of the license can be identified by inquiry made to the Contractor or DOE. NEITHER CONTRACTOR, THE UNITED STATES, NOR THE UNITED STATES DEPARTMENT OF ENERGY, NOR ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF ANY DATA, APPARATUS, PRODUCT, OR PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED RIGHTS.

# LICENSE
[LICENSE](LICENSE)

# Citation
Kee, Jamie, Penev, Michael, and USDOE Office of Energy Efficiency and Renewable Energy. ProFAST (Production Financial Analysis Scenario Tool) [SWR-23-88]. Computer software. USDOE Office of Energy Efficiency and Renewable Energy (EERE), Office of Sustainable Transportation. Hydrogen Fuel Cell Technologies Office (HFTO). 9 Nov. 2023. Web. doi:10.11578/dc.20231211.1.

# Setup
ProFAST can be installed using pip. Refer to [pyproject.toml](pyproject.toml) for configuration. ProFAST is installed as a compiled python file.

## Installation
`$ pip install .`

## Testing
`$ pytest`


# Quick Start Example

This quick start example is also in [generic_example.py](ProFAST/examples/generic_example.py) and can be accessed for exmaple usage.

Start by importing the ProFAST class from the ProFAST package

```python
from ProFAST import ProFAST
```

Initialize a ProFAST instance

```python
pf = ProFAST()
```

Set parameter values for the financial model (you set some of them to 0 or not set them at all)
```python
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
```


Set the feedstocks
```python
pf.add_feedstock(name='Water',usage=3.78,unit='gal',cost=0.005,escalation=gen_inflation) #3.78gal/kg H2
pf.add_feedstock(name='Electricity (industrial)',usage=55.5,unit='kWh',cost=0.15,escalation=gen_inflation)
```

You can also use dictionaries and list to set the usages and costs
```python
years = list(map(str,range(2025-1,2025+30+2)))
elec_usage = np.linspace(55.5,65,len(years))
elec_usage_dict = dict(zip(years,elec_usage))
pf.add_feedstock(name='Electricity (industrial) dict',usage=elec_usage_dict,unit='kWh',cost=0.15,escalation=gen_inflation)
pf.remove_feedstock(name='Electricity (industrial) dict')
```

You can also use AEO feedstocks (Name and Cost must be valid values from AEO list)
```python
pf.edit_feedstock(name='Electricity (industrial)',value={'cost':'Mountain'})
# AEO feedstocks can be modified for sensitivity analysis
pf.edit_feedstock(name='Electricity (industrial)',value={'usage':55.5,'cost':'1.1X Mountain'})
```

Set the coproducts
```python
pf.add_coproduct(name='Oxygen',usage=7,unit='mol',cost=0.01,escalation=gen_inflation) 
pf.edit_coproduct(name='Oxygen',value={'usage':7})
```


Set the capital items. These have a depreciation and a refurbishment schedule
```python
dol_per_kw = 500
kW = 50000/24*55.5
pf.add_capital_item(name='PEM Stack',cost=kW*dol_per_kw,depr_type='MACRS',depr_period=7,refurb=[0,0,0,0,0,0,0.15]*4) # Refurb 15% every 7 years
pf.add_capital_item(name='BOP',cost=1000000,depr_type='MACRS',depr_period=7,refurb=[0])
```


Set the fixed costs. which is a annual cost
```python
pf.add_fixed_cost(name='Fixed costs',usage=1,unit='$',cost=3000000,escalation=gen_inflation)
```

Set the incentives, which is a per unit commodity based incentive
```python
pf.add_incentive(name='PTC',value=3,decay=0,sunset_years=10,tax_credit=True)
```

This solves for the break even price - access it with ``sol["price"]``

```python
sol = pf.solve_price()

unit = pf.vals['commodity']['unit']
name = pf.vals['commodity']['name']
print('\n')
print(f'Levelized cost of {name} price: ${round(sol["lco"],2)}/{unit}')
print('\n')
```

Plot the cost breakdowns
```python
pf.plot_costs()
```

# Premade files
Refer to the resources directory for premade JSON files to load in a ProFAST instance, where the input parameter is the filename. For example, to load in a sample [central grid electrolysis PEM](ProFAST/resources/central_grid_electrolysis_PEM.json)
```python
pf = ProFAST('central_grid_electrolysis_PEM')
```

