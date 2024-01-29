import xlwings as xw
import ProFAST
import random 
import numpy as np
from pkg_resources import resource_filename
import json,csv

def gen_hard_coded_vals(filename):
    wb = xw.Book(filename)
    sheet = wb.sheets['Interface']
    
    sheet['D29'].value = '=BreakEven'

    NPV_cell = 'D9'

    sheet[NPV_cell].number_format = 'General'

    pf = ProFAST.ProFAST('only_variables')

    cell_locs = {'capacity':'D26',
                'installation cost':{'value':'D66','depr type':'E66','depr period':'F66','depreciable':'D172'},
                'non depr assets':'D67',
                'end of proj sale non depr assets':'D68',
                'maintenance':{'value':'D156','escalation':'D157'},
                'one time cap inct':{'value':'D38','depr type':'E38','depr period':'F38','depreciable':'D174'},
                'annual operating incentive':{'value':'D39','decay':'D40','sunset years':'D41','taxable':'D173'},
                'incidental revenue':{'value':'D52','escalation':'D53'},
                'commodity':{'name':'D23','unit':'D24','initial price':'D29','escalation':'D30'},
                'analysis start year':'D31',
                'operating life':'D32',
                'installation months':'D33',
                'demand rampup':'D34',
                'long term utilization':'D35',
                'TOPC':{'unit price':'D48','decay':'D49','sunset years':'D50','support utilization':'D51'},
                'credit card fees':'D143',
                'sales tax':'D144',
                'road tax':{'value':'D145','escalation':'D146'},
                'labor':{'value':'D147','rate':'D148','escalation':'D149'},
                'license and permit':{'value':'D150','escalation':'D151'},
                'rent':{'value':'D152','escalation':'D153'},
                'property tax and insurance':'D154',
                'admin expense':'D155',
                'total income tax rate':'D170',
                'capital gains tax rate':'D171',
                'sell undepreciated cap':'D175',
                'tax losses monetized':'D176',
                'tax loss carry forward years':'F177',
                'general inflation rate':'D178',
                'leverage after tax nominal discount rate':'D181',
                'debt equity ratio of initial financing':'D182',
                'debt type':'D183',
                'loan period if used':'D184',
                'debt interest rate':'D185',
                'cash onhand':'D186',
                'fraction of capital spent in constr year':'D69'
    }

    with open('ProFAST/resources/only_variables.json') as json_file:
        def_val = json.load(json_file)['variables']
    # print(def_val)
    #Set to these default values
    for i in def_val:
        # print(i)
        if isinstance(def_val[i],dict):
            pf_dict = def_val[i].copy()
            for j in def_val[i]:
                if j == 'initial price':
                    continue
                val = def_val[i][j]
                if j=='depreciable' or j=='taxable':
                    val = 'Yes' if val else 'No'
                sheet[cell_locs[i][j]].value = val
                # pf_dict[j] = val if j != 'depreciable' else val=='Yes'
            # pf.set_params(i,pf_dict)
            # print(f'\t{pf_dict}')
        else:
            val = def_val[i]
            if i in ['tax losses monetized','sell undepreciated cap']:
                val = 'Yes' if val else 'No'
            if i == 'debt type':
                val = 'Bond debt' if val=='Revolving debt' else 'No'

            sheet[cell_locs[i]].value = val
            # pf_val = val
            # if i in ['tax losses monetized','operating incentives taxable','sell undepreciated cap']:
            #     pf_val = val=='Yes' 
            # if i == 'debt type':
            #     pf_val = 'Revolving debt' if val == 'Bond debt' else val
            # print(f'\t{pf_val}')
            # pf.set_params(i,pf_val)
    for i in range(10):
        set_capital(sheet,f'Capital item {i}',0,'MACRS',7,i)

        #   Set feedstocks
    for i in range(15):
        set_feedstock(sheet,f'Feedstock {i}',0,0,0,i)
        #   Set coprods
    for i in range(6):
        set_coprod(sheet,f'Coprod {i}',0,0,0.00,i) 

        #   Set fixed costs
    for i in range(10):
        set_fixedcost(sheet,f'Fixed cost {i}',0,0.00,i) 

        #   Set incentives
    for i in range(10):
        set_incentive(sheet,f'Incentive {i}',0,'Income',0.00,0,i)

    save_vals = []
    names = []

    # initialize
    names.append('initial load')
    save_vals.append(sheet[NPV_cell].value)
    
    # Test adding capital MACRS
    name = 'Capital test'
    val = 1000000
    depr_type = 'MACRS'
    depr_period = 5
    set_capital(sheet,name,val,depr_type,depr_period,i)
    save_vals.append(sheet[NPV_cell].value)
    set_capital(sheet,name,0,depr_type,depr_period,i)

    # Test adding capital straight line
    name = 'Capital test'
    val = 1000000
    depr_type = 'Straight line'
    depr_period = 5
    set_capital(sheet,name,val,depr_type,depr_period,i)
    save_vals.append(sheet[NPV_cell].value)
    set_capital(sheet,name,0,depr_type,depr_period,i)

    # Test adding capital period
    name = 'Capital test'
    val = 1000000
    depr_type = 'MACRS'
    depr_period = 7
    set_capital(sheet,name,val,depr_type,depr_period,0)
    save_vals.append(sheet[NPV_cell].value)
    set_capital(sheet,name,0,depr_type,depr_period,0)

    # Test modifying capital 
    name = 'Capital test'
    val = 2000000
    depr_type = 'MACRS'
    depr_period = 10
    set_capital(sheet,name,val,depr_type,depr_period,0)
    save_vals.append(sheet[NPV_cell].value)
    set_capital(sheet,name,0,depr_type,depr_period,0)

    # Test adding multiple capital
    depr_type = 'MACRS'
    set_capital(sheet,'Capital test1',1000000,depr_type,7,0)
    set_capital(sheet,'Capital test2',2000000,depr_type,5,1)
    save_vals.append(sheet[NPV_cell].value)
    set_capital(sheet,name,0,depr_type,depr_period,0)
    set_capital(sheet,name,0,depr_type,depr_period,1)

    # Test adding feedstock
    name = 'Feedstock test'
    usage = 1
    cost = 1
    escalation = 0.01
    set_feedstock(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_feedstock(sheet,name,0,cost,escalation,0)

    # Test adding feedstock - usage
    name = 'Feedstock test'
    usage = 3
    cost = 1
    escalation = 0.01
    set_feedstock(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_feedstock(sheet,name,0,cost,escalation,0)

    # Test adding feedstock - cost
    name = 'Feedstock test'
    usage = 1
    cost = 2
    escalation = 0.01
    set_feedstock(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_feedstock(sheet,name,0,cost,escalation,0)

    # Test adding feedstock - escalation
    name = 'Feedstock test'
    usage = 1
    cost = 2
    escalation = 0.05
    set_feedstock(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_feedstock(sheet,name,0,cost,escalation,0)

    # Test adding feedstock - x2
    name = 'Feedstock test'
    usage = 1
    cost = 2
    escalation = 0.05
    set_feedstock(sheet,'Feedstock test 1',1,1,0.01,0)
    set_feedstock(sheet,'Feedstock test 2',3,3,0.03,1)
    save_vals.append(sheet[NPV_cell].value)
    set_feedstock(sheet,name,0,cost,escalation,0)
    set_feedstock(sheet,name,0,cost,escalation,1)

    # Test adding coproduct
    name = 'Coproduct test'
    usage = 1
    cost = 1
    escalation = 0.01
    set_coprod(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_coprod(sheet,name,0,cost,escalation,0)

    # Test adding coproduct - usage
    name = 'Coproduct test'
    usage = 2
    cost = 1
    escalation = 0.01
    set_coprod(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_coprod(sheet,name,0,cost,escalation,0)

    # Test adding coproduct - cost
    name = 'Coproduct test'
    usage = 1
    cost = 2
    escalation = 0.01
    set_coprod(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_coprod(sheet,name,0,cost,escalation,0)

    # Test adding coproduct - escalation
    name = 'Coproduct test'
    usage = 1
    cost = 1
    escalation = 0.02
    set_coprod(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_coprod(sheet,name,0,cost,escalation,0)

    # Test modifying coproduct
    name = 'Coproduct test'
    usage = 2
    cost = 2
    escalation = 0.01
    set_coprod(sheet,name,usage,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_coprod(sheet,name,0,cost,escalation,0)

    # Test adding coproduct x2
    set_coprod(sheet,'Coproduct test 1',1,1,0.01,0)
    set_coprod(sheet,'Coproduct test 2',2,2,0.02,1)
    save_vals.append(sheet[NPV_cell].value)
    set_coprod(sheet,name,0,cost,escalation,0)
    set_coprod(sheet,name,0,cost,escalation,1)

    # Test adding incentive
    name = 'Incentive test'
    value = 1
    years = 5
    escalation = 0.01
    tc = 'Tax credit'
    set_incentive(sheet,name,value,tc,escalation,years,0)
    save_vals.append(sheet[NPV_cell].value)
    set_incentive(sheet,name,0,tc,escalation,years,0)

    # Test adding incentive - value
    name = 'Incentive test'
    value = 2
    years = 5
    escalation = 0.01
    tc = 'Tax credit'
    set_incentive(sheet,name,value,tc,escalation,years,0)
    save_vals.append(sheet[NPV_cell].value)
    set_incentive(sheet,name,0,tc,escalation,years,0)

    # Test adding incentive - decay
    name = 'Incentive test'
    value = 1
    years = 5
    escalation = 0.05
    tc = 'Tax credit'
    set_incentive(sheet,name,value,tc,escalation,years,0)
    save_vals.append(sheet[NPV_cell].value)
    set_incentive(sheet,name,0,tc,escalation,years,0)

    # Test adding incentive - ss years
    name = 'Incentive test'
    value = 1
    years = 7
    escalation = 0.01
    tc = 'Tax credit'
    set_incentive(sheet,name,value,tc,escalation,years,0)
    save_vals.append(sheet[NPV_cell].value)
    set_incentive(sheet,name,0,tc,escalation,years,0)

    # Test adding incentive
    name = 'Incentive test'
    value = 1
    years = 5
    escalation = 0.01
    tc = 'Income'
    set_incentive(sheet,name,value,tc,escalation,years,0)
    save_vals.append(sheet[NPV_cell].value)
    set_incentive(sheet,name,0,tc,escalation,years,0)

    # Test adding incentive
    name = 'Incentive test'
    value = 2
    years = 3
    escalation = -0.01
    tc = 'Tax credit'
    set_incentive(sheet,name,value,tc,escalation,years,0)
    save_vals.append(sheet[NPV_cell].value)
    set_incentive(sheet,name,0,tc,escalation,years,0)

    # Test adding incentive
    set_incentive(sheet,'Incentive test 1',1,'Tax credit',0.01,5,0)
    set_incentive(sheet,'Incentive test 1',2,'Income',0.05,7,1)
    save_vals.append(sheet[NPV_cell].value)
    set_incentive(sheet,name,0,tc,escalation,years,0)
    set_incentive(sheet,name,0,tc,escalation,years,1)

    # Test adding fixed cost
    name = 'Fixed cost test'
    cost = 1000
    escalation = 0.01
    set_fixedcost(sheet,name,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_fixedcost(sheet,name,0,escalation,0)

    # Test adding fixed cost cost
    name = 'Fixed cost test'
    cost = 5000
    escalation = 0.01
    set_fixedcost(sheet,name,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_fixedcost(sheet,name,0,escalation,0)

    # Test adding fixed cost escalation
    name = 'Fixed cost test'
    cost = 1000
    escalation = 0.05
    set_fixedcost(sheet,name,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_fixedcost(sheet,name,0,escalation,0)

    # Test modify fixed cost 
    name = 'Fixed cost test'
    cost = 5000
    escalation = 0.05
    set_fixedcost(sheet,name,cost,escalation,0)
    save_vals.append(sheet[NPV_cell].value)
    set_fixedcost(sheet,name,0,escalation,0)

    # Test adding fixed cost x2
    set_fixedcost(sheet,'Fixed cost test 1',1000,0.01,0)
    set_fixedcost(sheet,'Fixed cost test 2',5000,0.05,1)
    save_vals.append(sheet[NPV_cell].value)
    set_fixedcost(sheet,name,0,escalation,0)
    set_fixedcost(sheet,name,0,escalation,1)


    #   Loop thru variables and edit
    for i in def_val:
        print (i)
        if isinstance(def_val[i],dict):
            for j in def_val[i]:
                print(f'\t{j}')
                if j in ['initial price','name','unit']:
                    continue
                if j=='depr period':
                    continue
                original_val = def_val[i][j]
                val = def_val[i][j]
                if j=='depreciable' or j=='taxable':
                    val = 'Yes' if not val else 'No'
                    original_val = 'Yes' if original_val else 'No'
                elif j=='depr type':
                    val = 'MACRS' if val=='Straight line' else 'Straight line'
                    depr_orig= sheet[cell_locs[i]['depr period']].value
                    sheet[cell_locs[i][j]].value = val
                    sheet[cell_locs[i]['depr period']].value = 7
                    save_vals.append(sheet[NPV_cell].value)
                    sheet[cell_locs[i][j]].value = original_val
                    sheet[cell_locs[i]['depr period']].value = depr_orig
                    continue
                else:
                    val = val*1.5
                sheet[cell_locs[i][j]].value = val
                save_vals.append(sheet[NPV_cell].value)
                sheet[cell_locs[i][j]].value = original_val
                print(f'\t{val}',f'\t{original_val}')
        else:
            val = def_val[i]
            original_val = def_val[i]
            if i in ['tax losses monetized','sell undepreciated cap']:
                val = 'Yes' if not val else 'No'
                original_val = 'Yes' if original_val else 'No'
            elif i == 'debt type':
                val = 'Bond debt' if val!='Revolving debt' else 'One time loan'
                original_val = 'Bond debt' if original_val=='Revolving debt' else 'One time loan'
            elif i == 'long term utilization':
                val = 0.95
            elif i == 'installation months':
                val = 15
            elif  i == 'loan period if used':
                val = 7
            else:
                val = val*1.5
            print(f'\t{val}',f'\t{original_val}')
            sheet[cell_locs[i]].value = val
            save_vals.append(sheet[NPV_cell].value)
            sheet[cell_locs[i]].value = original_val


    file = open('tests/hard_coded.csv', 'w+', newline ='')
    with file:   
        write = csv.writer(file)
        write.writerows([save_vals])

def random_excel_comparison(filename):
    '''
        This function randomize inputs and compare the break even price to the excel workbook
    '''
    wb = xw.Book(filename)
    sheet = wb.sheets['Interface']
    
    sheet['D29'].value = '=BreakEven'

    NPV_cell = 'D9'

    sheet[NPV_cell].number_format = 'General'

    cell_locs = {'capacity':'D26',
                'installation cost':{'value':'D66','depr type':'E66','depr period':'F66','depreciable':'D172'},
                'non depr assets':'D67',
                'end of proj sale non depr assets':'D68',
                'maintenance':{'value':'D156','escalation':'D157'},
                'one time cap inct':{'value':'D38','depr type':'E38','depr period':'F38','depreciable':'D174'},
                'annual operating incentive':{'value':'D39','decay':'D40','sunset years':'D41','taxable':'D173'},
                'incidental revenue':{'value':'D52','escalation':'D53'},
                'commodity':{'name':'D23','unit':'D24','initial price':'D29','escalation':'D30'},
                'analysis start year':'D31',
                'operating life':'D32',
                'installation months':'D33',
                'demand rampup':'D34',
                'long term utilization':'D35',
                'TOPC':{'unit price':'D48','decay':'D49','sunset years':'D50','support utilization':'D51'},
                'credit card fees':'D143',
                'sales tax':'D144',
                'road tax':{'value':'D145','escalation':'D146'},
                'labor':{'value':'D147','rate':'D148','escalation':'D149'},
                'license and permit':{'value':'D150','escalation':'D151'},
                'rent':{'value':'D152','escalation':'D153'},
                'property tax and insurance':'D154',
                'admin expense':'D155',
                'total income tax rate':'D170',
                'capital gains tax rate':'D171',
                'sell undepreciated cap':'D175',
                'tax losses monetized':'D176',
                'tax loss carry forward years':'F177',
                'general inflation rate':'D178',
                'leverage after tax nominal discount rate':'D181',
                'debt equity ratio of initial financing':'D182',
                'debt type':'D183',
                'loan period if used':'D184',
                'debt interest rate':'D185',
                'cash onhand':'D186',
                'fraction of capital spent in constr year':'D69'
    }

    def_val = {'capacity':10000,
                'installation cost':{"value":1632845.8409,"depr type":"Straight line","depr period":4,"depreciable":False},
                'non depr assets':632845.8409,
                'end of proj sale non depr assets':989250.8911,
                'maintenance':{'value':172507.0742,"escalation":0.013868566},
                'one time cap inct':{"value":2119203.192,"depr type":"MACRS","depr period":5,"depreciable":True},
                'annual operating incentive':{"value":163673.7733,"decay":0.034906267,"sunset years":6,"taxable":True},
                'incidental revenue':{"value":6951.098006,"escalation":0.025771},
                'commodity':{'initial price':20.1234,'name':'Hydrogen','unit':'kg','escalation':0.02618},
                'analysis start year':2020,
                'operating life':16,
                'installation months':37,
                'demand rampup':5.6543,
                'long term utilization':0.70849,
                'TOPC':{"unit price":0.822668382,"decay":0.05084,"support utilization":0.6787,"sunset years":3},
                'credit card fees':0.024271134,
                'sales tax':0.024207775,
                'road tax':{"value":0.753892586,"escalation":0.0261},
                'labor':{"value":2956.583883,"rate":17.71964046,"escalation":0.0387},
                'license and permit':{"value":399.1349058,"escalation":0.010526704},
                'rent':{"value":19470.00933,"escalation":0.001743845},
                'property tax and insurance':0.048568935,
                'admin expense':0.003785587,
                'total income tax rate':0.33874403,
                'capital gains tax rate':0.118755993,
                'sell undepreciated cap':True,
                'tax losses monetized':True,
                'tax loss carry forward years':7,
                'general inflation rate':0.01782,
                'leverage after tax nominal discount rate':0.109284877,
                'debt equity ratio of initial financing':0.919458823,
                'debt type':'Revolving debt',
                'loan period if used':15,
                'debt interest rate':0.082953591,
                'cash onhand':0.823394427,
                # 'fraction of capital spent in constr year':1
                }

        

    # #   Setting defaults
    #     #   Set variables
    # for i in cell_locs:
    #     if isinstance(cell_locs[i],dict):
    #         for j in cell_locs[i]:
    #             sheet[cell_locs[i][j]].value = def_val[i][j]
    #     else:
    #         sheet[cell_locs[i]].value = def_val[i]
    #     #   Set capital
    # for i in range(10):
    #     set_capital(sheet,f'Capital item {i}',0,'MACRS',7,i)

    #     #   Set feedstocks
    # for i in range(15):
    #     set_feedstock(sheet,f'Feedstock {i}',0,0,0,i)
    #     #   Set coprods
    # for i in range(6):
    #     set_coprod(sheet,f'Coprod {i}',10,20,0.02,i) 

    #     #   Set fixed costs
    # for i in range(10):
    #     set_fixedcost(sheet,f'Fixed cost {i}',20,0.02,i) 

    #     #   Set incentives
    # for i in range(10):
    #     set_incentive(sheet,f'Incentive {i}',1,'Income',0.02,10,i)


    val_ranges = {'capacity':np.arange(1000,1000000),
                'installation cost':{"value":np.arange(1000,1000000),"depr type":["Straight line","MACRS"],"depr period":[3,5,7,10,15,20],"depreciable":['Yes','No']},
                'non depr assets':np.arange(1000,1000000),
                'end of proj sale non depr assets':np.arange(1000,1000000),
                'maintenance':{'value':np.arange(1000,1000000),"escalation":np.arange(0.0,1.0,0.05)},
                'one time cap inct':{"value":np.arange(1000,1000000),"depr type":["Straight line","MACRS"],"depr period":[3,5,7,10,15,20],"depreciable":['Yes','No']},
                'annual operating incentive':{"value":np.arange(1000,1000000),"decay":np.arange(0,1,0.05),"sunset years":np.arange(1,10)},
                'incidental revenue':{"value":np.arange(1000,1000000),"escalation":np.arange(0,1,0.05)},
                'commodity':{'initial price':np.arange(1,5),'name':['Hydrogen'],'unit':['kg'],'escalation':np.arange(0,1,0.05)},
                'analysis start year':np.arange(2015,2030),
                'operating life':np.arange(8,40),
                'installation months':np.arange(12,40),
                'demand rampup':np.arange(1,7,0.5),
                'long term utilization':np.arange(0.1,1,0.05),
                'TOPC':{"unit price":np.arange(0,5,0.5),"decay":np.arange(0,1,0.05),"support utilization":np.arange(0.1,1,0.05),"sunset years":np.arange(1,10)},
                'credit card fees':np.arange(0,0.25,0.05),
                'sales tax':np.arange(0,0.25,0.05),
                'road tax':{"value":np.arange(0,0.5,0.05),"escalation":np.arange(0,1,0.05)},
                'labor':{"value":np.arange(100,3000),"rate":np.arange(5,25,0.5),"escalation":np.arange(0,1,0.05)},
                'license and permit':{"value":np.arange(10,3000),"escalation":np.arange(0,1,0.05)},
                'rent':{"value":np.arange(1000,30000),"escalation":np.arange(0,1,0.05)},
                'property tax and insurance':np.arange(0.01,0.1,0.005),
                'admin expense':np.arange(0.01,0.1,0.005),
                'total income tax rate':np.arange(0.01,0.5,0.05),
                'capital gains tax rate':np.arange(0.01,0.1,0.005),
                'sell undepreciated cap':['Yes','No'],
                'tax losses monetized':['Yes','No'],
                'tax loss carry forward years':np.arange(1,7),
                'general inflation rate':np.arange(0.01,0.1,0.005),
                'leverage after tax nominal discount rate':np.arange(0,0.1,0.005),
                'debt equity ratio of initial financing':np.arange(0.5,1.5,0.05),
                'debt type':['One time loan','Bond debt'],
                'loan period if used':np.arange(1,15),
                'debt interest rate':np.arange(0.01,0.1,0.005),
                'cash onhand':np.arange(0.5,10,0.05),
                # 'fraction of capital spent in constr year':[1]
                }
    

    pf = ProFAST.ProFAST('blank')
    
    for i in val_ranges:
        print(i)
        if isinstance(val_ranges[i],dict):
            pf_dict = val_ranges[i].copy()
            for j in val_ranges[i]:
                if j == 'initial price':
                    continue
                val = random.choice(val_ranges[i][j])
                sheet[cell_locs[i][j]].value = val
                pf_dict[j] = val if j != 'depreciable' else val=='Yes'
            pf.set_params(i,pf_dict)
            print(f'\t{pf_dict}')
        else:
            val = random.choice(val_ranges[i])
            sheet[cell_locs[i]].value = val

            pf_val = val
            if i in ['tax losses monetized','sell undepreciated cap']:
                pf_val = val=='Yes' 
            if i == 'debt type':
                pf_val = 'Revolving debt' if val == 'Bond debt' else val
            print(f'\t{pf_val}')
            pf.set_params(i,pf_val)
    
    #   Set capital
    for i in range(10):
        name = f'Capital item {i}'
        val = random.choice(np.arange(100,100000))
        depr_type = random.choice(['MACRS','Straight line'])
        depr_period = random.choice([3,5,7,10,15,20])

        set_capital(sheet,name,val,depr_type,depr_period,i)

        pf.add_capital_item(name,val,depr_type,depr_period,refurb=[0])

    #   Set feedstocks
    for i in range(15):
        name = f'Feedstock {i}'
        usage = random.choice(np.arange(0.01,10,0.05))
        cost = random.choice(np.arange(0.5,10,0.05))
        escalation = random.choice(np.arange(0.0,0.25,0.05))
        set_feedstock(sheet,name,usage,cost,escalation,i)
        pf.add_feedstock(name,usage,'',cost,escalation)
        
    #   Set coprods
    for i in range(6):
        name = f'Coprod {i}'
        usage = random.choice(np.arange(0.01,10,0.05))
        cost = random.choice(np.arange(0.5,10,0.05))
        escalation = random.choice(np.arange(0.0,0.25,0.05))
        set_coprod(sheet,name,usage,cost,escalation,i) 
        pf.add_coproduct(name,usage,'',cost,escalation)

    #   Set fixed costs
    for i in range(5):
        name = f'Fixed cost {i}'
        cost = random.choice(np.arange(100,10000,100))
        escalation = random.choice(np.arange(0.0,0.25,0.05))
        set_fixedcost(sheet,name,cost,escalation,i) 
        pf.add_fixed_cost(name,1,'',cost,escalation)

    #   Set incentives
    for i in range(2):
        name = f'Incentive {i}'
        value = random.choice(np.arange(0.01,1,0.01))
        tax_creditable = random.choice([True,False])
        escalation = random.choice(np.arange(0.0,0.25,0.05))
        sunset_years = random.choice(np.arange(0,10))
        set_incentive(sheet,name,value,'Tax credit' if tax_creditable else 'Income',escalation,sunset_years,i)
        pf.add_incentive(name,value,-1*escalation,sunset_years,tax_creditable)

    print(f'ProFAST: {sheet[NPV_cell].value}')

    sol = pf.solve_price()
    print(f'PyFAST: {sol["price"]}')

def run_comparison():
    pf = ProFAST.ProFAST('blank')


        

if __name__ == "__main__":
    def set_capital(sheet,name,val,depr_type,depr_period,index):
        row = 56+index
        if index>9:
            return
        
        sheet[f'C{row}'].value = name
        sheet[f'D{row}'].value = val
        sheet[f'E{row}'].value = depr_type
        sheet[f'F{row}'].value = depr_period
        
    def set_feedstock(sheet,name,usage,cost,escalation,index):
        row  = 72+index
        row2 = 97+index*2
        if index>14:
            return
        
        sheet[f'E{row}'].value = name
        sheet[f'D{row}'].value = usage
        sheet[f'D{row2}'].value = cost
        sheet[f'D{row2+1}'].value = escalation

    def set_coprod(sheet,name,usage,cost,escalation,index):
        row  = 89+index
        row2 = 129+index*2
        if index>5:
            return
        
        sheet[f'E{row}'].value = name
        sheet[f'D{row}'].value = usage
        sheet[f'D{row2}'].value = cost
        sheet[f'D{row2+1}'].value = escalation

    def set_fixedcost(sheet,name,cost,escalation,index):
        row  = 158+index*2
        if index>5:
            return

        sheet[f'F{row}'].value = name
        sheet[f'D{row}'].value = cost
        sheet[f'D{row+1}'].value = escalation

    def set_incentive(sheet,name,value,type,escalation,years,index):
        row  = 42+index*3
        if index>1:
            return

        sheet[f'F{row}'].value = name
        sheet[f'D{row}'].value = value
        sheet[f'E{row}'].value = type
        sheet[f'D{row+1}'].value = escalation
        sheet[f'D{row+2}'].value = years

    filename = resource_filename(__name__, f'../ProFAST/resources/h2-fast-2022-07202023-generic-fueling.xlsm')
    gen_hard_coded_vals(filename)