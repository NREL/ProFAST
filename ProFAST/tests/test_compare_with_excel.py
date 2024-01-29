import ProFAST
import csv

import pytest

"""
Compare PyFAST with pfAST hardcoded values
Note: Bug found in pfAST 2022-09-20, need to update values - only relevant for op years over 36
Note: Incentive income calculation has changed with ProFAST update. Need to update
Note: re-written in pytest format by Jared T. 2022-11-30
:param None
:return None
"""

class TestCompareExcel():
    with open('tests/hard_coded.csv', newline='') as f:
        reader = csv.reader(f)
        hard_coded = list(reader)[0]
        hard_coded = [float(x) for x in hard_coded]
    # hard_coded = pd.read_csv('tests/hard_coded.csv').tolist()

    pf = ProFAST.ProFAST('only_variables')

class TestInitial(TestCompareExcel):
    def test_init(self):
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[0])

class TestCapitalItems(TestCompareExcel):
    def test_adding_capital(self):
        self.pf.add_capital_item('Test item 1',1000000,'MACRS',5,[0])
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[1])

    def test_removing_capital(self):
        self.pf.remove_capital_item('Test item 1')
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[0])

    def test_adding_capital_SL(self):
        self.pf.add_capital_item('Test item 1',1000000,'Straight line',5,[0])
        sol=self.pf.solve_price()
        self.pf.remove_capital_item('Test item 1')
        assert sol['price'] == pytest.approx(self.hard_coded[2])

    def test_adding_capital_depr_period(self):
        self.pf.add_capital_item('Test item 1',1000000,'MACRS',7,[0])
        self.pf.edit_capital_item('Test item 1',{'cost':2000000,'depr_period':10})
        sol=self.pf.solve_price()
        self.pf.remove_capital_item('Test item 1')
        assert sol['price'] == pytest.approx(self.hard_coded[4])

    def test_adding_capital_x2(self):
        self.pf.add_capital_item('Test item 1',1000000,'MACRS',7,[0])
        self.pf.add_capital_item('Test item 2',2000000,'MACRS',5,[0])
        sol=self.pf.solve_price()
        self.pf.remove_capital_item('Test item 1')
        self.pf.remove_capital_item('Test item 2')
        assert sol['price'] == pytest.approx(self.hard_coded[5])

class TestFeedstocks(TestCompareExcel):
    def test_adding_feedstock(self):
        self.pf.add_feedstock(name='Feedstock test 1',usage=1,unit='kg',cost=1,escalation=0.01)
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[6])

    def test_removing_feedstock(self):
        self.pf.remove_feedstock('Feedstock test 1')
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[0])

    def test_adding_feedstock_usage(self):
        self.pf.add_feedstock(name='Feedstock test 1',usage=3,unit='kg',cost=1,escalation=0.01)
        sol=self.pf.solve_price()
        self.pf.remove_feedstock('Feedstock test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[7])

    def test_adding_feedstock_cost(self):
        self.pf.add_feedstock(name='Feedstock test 1',usage=1,unit='kg',cost=2,escalation=0.01)
        sol=self.pf.solve_price()
        self.pf.remove_feedstock('Feedstock test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[8])

    def test_adding_feedstock_escalation(self):
        self.pf.add_feedstock(name='Feedstock test 1',usage=1,unit='kg',cost=2,escalation=0.05)
        sol=self.pf.solve_price()
        self.pf.remove_feedstock('Feedstock test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[9])

    def test_modifying_feedstock(self):
        self.pf.add_feedstock(name='Feedstock test 1',usage=1,unit='kg',cost=1,escalation=0.01)
        self.pf.edit_feedstock('Feedstock test 1',{'cost':2,'escalation':0.05})
        sol=self.pf.solve_price()
        self.pf.remove_feedstock('Feedstock test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[9])

    def test_adding_feedstock_x2(self):
        self.pf.add_feedstock(name='Feedstock test 1',usage=1,unit='kg',cost=1,escalation=0.01)
        self.pf.add_feedstock(name='Feedstock test 2',usage=3,unit='kg',cost=3,escalation=0.03)
        sol=self.pf.solve_price()
        self.pf.remove_feedstock('Feedstock test 1')
        self.pf.remove_feedstock('Feedstock test 2')
        assert sol['price'] == pytest.approx(self.hard_coded[10])

class TestCoproducts(TestCompareExcel):
    def test_adding_coproduct(self):
        self.pf.add_coproduct(name='Coprod test 1',usage=1,unit='kg',cost=1,escalation=0.01)
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[11])

    def test_removing_coproduct(self):
        self.pf.remove_coproduct(name='Coprod test 1')
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[0])

    def test_adding_coproduct_usage(self):
        self.pf.add_coproduct(name='Coprod test 1',usage=2,unit='kg',cost=1,escalation=0.01)
        sol=self.pf.solve_price()
        self.pf.remove_coproduct('Coprod test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[12])

    def test_adding_coproduct_cost(self):
        self.pf.add_coproduct(name='Coprod test 1',usage=1,unit='kg',cost=2,escalation=0.01)
        sol=self.pf.solve_price()
        self.pf.remove_coproduct('Coprod test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[13])

    def test_adding_coproduct_escalation(self):
        self.pf.add_coproduct(name='Coprod test 1',usage=1,unit='kg',cost=1,escalation=0.02)
        sol=self.pf.solve_price()
        self.pf.remove_coproduct('Coprod test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[14])

    def test_adding_coproduct_escalation(self):
        self.pf.add_coproduct(name='Coprod test 1',usage=1,unit='kg',cost=1,escalation=0.01)
        self.pf.edit_coproduct('Coprod test 1',{'cost':2,'usage':2})
        sol=self.pf.solve_price()
        self.pf.remove_coproduct('Coprod test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[15])

    def test_adding_coproduct_x2(self):
        self.pf.add_coproduct(name='Coprod test 1',usage=1,unit='kg',cost=1,escalation=0.01)
        self.pf.add_coproduct(name='Coprod test 2',usage=2,unit='kg',cost=2,escalation=0.02)
        sol=self.pf.solve_price()
        self.pf.remove_coproduct('Coprod test 1')
        self.pf.remove_coproduct('Coprod test 2')
        assert sol['price'] == pytest.approx(self.hard_coded[16])
    
class TestIncentives(TestCompareExcel):
    def test_adding_incentive(self):
        self.pf.add_incentive(name='Incentive test 1',value=1,decay=-0.01,sunset_years=5,tax_credit=True)
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[17])

    def test_remove_incentive(self):
        self.pf.remove_incentive('Incentive test 1')
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[0])

    def test_adding_incentive_value(self):
        self.pf.add_incentive(name='Incentive test 1',value=2,decay=-0.01,sunset_years=5,tax_credit=True)
        sol=self.pf.solve_price()
        self.pf.remove_incentive('Incentive test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[18])

    def test_adding_incentive_decay(self):
        self.pf.add_incentive(name='Incentive test 1',value=1,decay=-0.05,sunset_years=5,tax_credit=True)
        sol=self.pf.solve_price()
        self.pf.remove_incentive('Incentive test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[19])

    def test_adding_incentive_sunset(self):
        self.pf.add_incentive(name='Incentive test 1',value=1,decay=-0.01,sunset_years=7,tax_credit=True)
        sol=self.pf.solve_price()
        self.pf.remove_incentive('Incentive test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[20])

    def test_adding_incentive_taxcredit(self):
        self.pf.add_incentive(name='Incentive test 1',value=1,decay=-0.01,sunset_years=5,tax_credit=False)
        sol=self.pf.solve_price()
        self.pf.remove_incentive('Incentive test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[21])

    def test_modify_incentive(self):
        self.pf.add_incentive(name='Incentive test 1',value=1,decay=-0.01,sunset_years=5,tax_credit=False)
        self.pf.edit_incentive('Incentive test 1',{'value':2,'decay':0.01,'sunset_years':3,'tax_credit':True})
        sol=self.pf.solve_price()
        self.pf.remove_incentive('Incentive test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[22])

    def test_adding_incentive_x2(self):
        self.pf.add_incentive(name='Incentive test 1',value=1,decay=-0.01,sunset_years=5,tax_credit=True)
        self.pf.add_incentive(name='Incentive test 2',value=2,decay=-0.05,sunset_years=7,tax_credit=False)
        sol=self.pf.solve_price()
        self.pf.remove_incentive('Incentive test 1')
        self.pf.remove_incentive('Incentive test 2')
        assert sol['price'] == pytest.approx(self.hard_coded[23])

class TestFixedCosts(TestCompareExcel):
    def test_adding_fixed_cost(self):
        self.pf.add_fixed_cost(name='Fixed cost test 1',usage=1,unit='$',cost=1000,escalation=0.01)
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[24])

    def test_remove_fixed_cost(self):
        self.pf.remove_fixed_cost('Fixed cost test 1')
        sol=self.pf.solve_price()
        assert sol['price'] == pytest.approx(self.hard_coded[0])

    def test_adding_fixed_cost_cost(self):
        self.pf.add_fixed_cost(name='Fixed cost test 1',usage=1,unit='$',cost=5000,escalation=0.01)
        sol=self.pf.solve_price()
        self.pf.remove_fixed_cost('Fixed cost test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[25])

    def test_adding_fixed_cost_escalation(self):
        self.pf.add_fixed_cost(name='Fixed cost test 1',usage=1,unit='$',cost=1000,escalation=0.05)
        sol=self.pf.solve_price()
        self.pf.remove_fixed_cost('Fixed cost test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[26])

    def test_modify_fixed_cost_cost(self):
        self.pf.add_fixed_cost(name='Fixed cost test 1',usage=1,unit='$',cost=1000,escalation=0.01)
        self.pf.edit_fixed_cost('Fixed cost test 1',{'cost':5000,'escalation':0.05})
        sol=self.pf.solve_price()
        self.pf.remove_fixed_cost('Fixed cost test 1')
        assert sol['price'] == pytest.approx(self.hard_coded[27])

    def test_adding_fixed_cost_x2(self):
        self.pf.add_fixed_cost(name='Fixed cost test 1',usage=1,unit='$',cost=1000,escalation=0.01)
        self.pf.add_fixed_cost(name='Fixed cost test 2',usage=1,unit='$',cost=5000,escalation=0.05)
        sol=self.pf.solve_price()
        self.pf.remove_fixed_cost('Fixed cost test 1')
        self.pf.remove_fixed_cost('Fixed cost test 2')
        assert sol['price'] == pytest.approx(self.hard_coded[28])

class TestParameters(TestCompareExcel):
    def test_capacity(self):
        original = self.pf.vals['capacity']
        self.pf.set_params('capacity',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('capacity',original)
        assert sol['price'] == pytest.approx(self.hard_coded[29])

    def test_utilization(self):
        original = self.pf.vals['long term utilization']
        self.pf.set_params('long term utilization',0.95)
        sol=self.pf.solve_price()
        self.pf.set_params('long term utilization',original)
        assert sol['price'] == pytest.approx(self.hard_coded[30])

    def test_demand_rampup(self):
        original = self.pf.vals['demand rampup']
        self.pf.set_params('demand rampup',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('demand rampup',original)
        assert sol['price'] == pytest.approx(self.hard_coded[31])

    def test_start_year(self):
        original = self.pf.vals['analysis start year']
        self.pf.set_params('analysis start year',int(original*1.5))
        sol=self.pf.solve_price()
        self.pf.set_params('analysis start year',original)
        assert sol['price'] == pytest.approx(self.hard_coded[32])

    def test_operating_life(self):
        original = self.pf.vals['operating life']
        self.pf.set_params('operating life',int(original*1.5))
        sol=self.pf.solve_price()
        self.pf.set_params('operating life',original)
        assert sol['price'] == pytest.approx(self.hard_coded[33])

    def test_installation_months(self):
        original = self.pf.vals['installation months']
        self.pf.set_params('installation months',15)
        sol=self.pf.solve_price()
        self.pf.set_params('installation months',original)
        assert sol['price'] == pytest.approx(self.hard_coded[34])

    def test_TOPC_price(self):
        original = self.pf.vals['TOPC']
        new = original.copy()
        new['unit price'] = original['unit price']*1.5
        self.pf.set_params('TOPC',new)
        sol=self.pf.solve_price()
        self.pf.set_params('TOPC',original)
        assert sol['price'] == pytest.approx(self.hard_coded[35])

    def test_TOPC_price(self):
        original = self.pf.vals['TOPC']
        new = original.copy()
        new['decay'] = original['decay']*1.5
        self.pf.set_params('TOPC',new)
        sol=self.pf.solve_price()
        self.pf.set_params('TOPC',original)
        assert sol['price'] == pytest.approx(self.hard_coded[36])

    def test_TOPC_util(self):
        original = self.pf.vals['TOPC']
        new = original.copy()
        new['support utilization'] = original['support utilization']*1.5
        self.pf.set_params('TOPC',new)
        sol=self.pf.solve_price()
        self.pf.set_params('TOPC',original)
        assert sol['price'] == pytest.approx(self.hard_coded[37])

    def test_TOPC_ssyrs(self):
        original = self.pf.vals['TOPC']
        new = original.copy()
        new['sunset years'] = original['sunset years']*1.5
        self.pf.set_params('TOPC',new)
        sol=self.pf.solve_price()
        self.pf.set_params('TOPC',original)
        assert sol['price'] == pytest.approx(self.hard_coded[38])

    def test_commodity_escalation(self):
        original = self.pf.vals['commodity']
        new = original.copy()
        new['escalation'] = original['escalation']*1.5
        self.pf.set_params('commodity',new)
        sol=self.pf.solve_price()
        self.pf.set_params('commodity',original)
        assert sol['price'] == pytest.approx(self.hard_coded[39])

    def test_ann_op_inct_value(self):
        original = self.pf.vals['annual operating incentive']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('annual operating incentive',new)
        sol=self.pf.solve_price()
        self.pf.set_params('annual operating incentive',original)
        assert sol['price'] == pytest.approx(self.hard_coded[40])

    def test_ann_op_inct_decay(self):
        original = self.pf.vals['annual operating incentive']
        new = original.copy()
        new['decay'] = original['decay']*1.5
        self.pf.set_params('annual operating incentive',new)
        sol=self.pf.solve_price()
        self.pf.set_params('annual operating incentive',original)
        assert sol['price'] == pytest.approx(self.hard_coded[41])

    def test_ann_op_inct_ssyears(self):
        original = self.pf.vals['annual operating incentive']
        new = original.copy()
        new['sunset years'] = original['sunset years']*1.5
        self.pf.set_params('annual operating incentive',new)
        sol=self.pf.solve_price()
        self.pf.set_params('annual operating incentive',original)
        assert sol['price'] == pytest.approx(self.hard_coded[42])

    def test_inc_rev_value(self):
        original = self.pf.vals['incidental revenue']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('incidental revenue',new)
        sol=self.pf.solve_price()
        self.pf.set_params('incidental revenue',original)
        assert sol['price'] == pytest.approx(self.hard_coded[44])

    def test_inc_rev_escalation(self):
        original = self.pf.vals['incidental revenue']
        new = original.copy()
        new['escalation'] = original['escalation']*1.5
        self.pf.set_params('incidental revenue',new)
        sol=self.pf.solve_price()
        self.pf.set_params('incidental revenue',original)
        assert sol['price'] == pytest.approx(self.hard_coded[45])

    def test_cc_fees(self):
        original = self.pf.vals['credit card fees']
        self.pf.set_params('credit card fees',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('credit card fees',original)
        assert sol['price'] == pytest.approx(self.hard_coded[46])

    def test_sales_tax(self):
        original = self.pf.vals['sales tax']
        self.pf.set_params('sales tax',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('sales tax',original)
        assert sol['price'] == pytest.approx(self.hard_coded[47])

    def test_road_tax_value(self):
        original = self.pf.vals['road tax']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('road tax',new)
        sol=self.pf.solve_price()
        self.pf.set_params('road tax',original)
        assert sol['price'] == pytest.approx(self.hard_coded[48])

    def test_road_tax_escalation(self):
        original = self.pf.vals['road tax']
        new = original.copy()
        new['escalation'] = original['escalation']*1.5
        self.pf.set_params('road tax',new)
        sol=self.pf.solve_price()
        self.pf.set_params('road tax',original)
        assert sol['price'] == pytest.approx(self.hard_coded[49])

    def test_labor_value(self):
        original = self.pf.vals['labor']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('labor',new)
        sol=self.pf.solve_price()
        self.pf.set_params('labor',original)
        assert sol['price'] == pytest.approx(self.hard_coded[50])

    def test_labor_rate(self):
        original = self.pf.vals['labor']
        new = original.copy()
        new['rate'] = original['rate']*1.5
        self.pf.set_params('labor',new)
        sol=self.pf.solve_price()
        self.pf.set_params('labor',original)
        assert sol['price'] == pytest.approx(self.hard_coded[51])

    def test_labor_escalation(self):
        original = self.pf.vals['labor']
        new = original.copy()
        new['escalation'] = original['escalation']*1.5
        self.pf.set_params('labor',new)
        sol=self.pf.solve_price()
        self.pf.set_params('labor',original)
        assert sol['price'] == pytest.approx(self.hard_coded[52])

    def test_maintenance_value(self):
        original = self.pf.vals['maintenance']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('maintenance',new)
        sol=self.pf.solve_price()
        self.pf.set_params('maintenance',original)
        assert sol['price'] == pytest.approx(self.hard_coded[53])

    def test_maintenance_escalation(self):
        original = self.pf.vals['maintenance']
        new = original.copy()
        new['escalation'] = original['escalation']*1.5
        self.pf.set_params('maintenance',new)
        sol=self.pf.solve_price()
        self.pf.set_params('maintenance',original)
        assert sol['price'] == pytest.approx(self.hard_coded[54])

    def test_rent_value(self):
        original = self.pf.vals['rent']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('rent',new)
        sol=self.pf.solve_price()
        self.pf.set_params('rent',original)
        assert sol['price'] == pytest.approx(self.hard_coded[55])

    def test_rent_escalation(self):
        original = self.pf.vals['rent']
        new = original.copy()
        new['escalation'] = original['escalation']*1.5
        self.pf.set_params('rent',new)
        sol=self.pf.solve_price()
        self.pf.set_params('rent',original)
        assert sol['price'] == pytest.approx(self.hard_coded[56])

    def test_license_permit_value(self):
        original = self.pf.vals['license and permit']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('license and permit',new)
        sol=self.pf.solve_price()
        self.pf.set_params('license and permit',original)
        assert sol['price'] == pytest.approx(self.hard_coded[57])

    def test_license_permit_escalation(self):
        original = self.pf.vals['license and permit']
        new = original.copy()
        new['escalation'] = original['escalation']*1.5
        self.pf.set_params('license and permit',new)
        sol=self.pf.solve_price()
        self.pf.set_params('license and permit',original)
        assert sol['price'] == pytest.approx(self.hard_coded[58])
    
    def test_non_depr_assets(self):
        original = self.pf.vals['non depr assets']
        self.pf.set_params('non depr assets',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('non depr assets',original)
        assert sol['price'] == pytest.approx(self.hard_coded[59])

    def test_sale_non_depr_assets(self):
        original = self.pf.vals['end of proj sale non depr assets']
        self.pf.set_params('end of proj sale non depr assets',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('end of proj sale non depr assets',original)
        assert sol['price'] == pytest.approx(self.hard_coded[60])

    def test_installation_cost_value(self):
        original = self.pf.vals['installation cost']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('installation cost',new)
        sol=self.pf.solve_price()
        self.pf.set_params('installation cost',original)
        assert sol['price'] == pytest.approx(self.hard_coded[61])

    def test_installation_cost_depr_type(self):
        original = self.pf.vals['installation cost']
        new = original.copy()
        new['depr type'] = 'MACRS' if original['depr type']=='Straight line' else 'Straight line'
        new['depr period'] = 7
        self.pf.set_params('installation cost',new)
        sol=self.pf.solve_price()
        self.pf.set_params('installation cost',original)
        assert sol['price'] == pytest.approx(self.hard_coded[62])

    def test_installation_cost_depreciable(self):
        original = self.pf.vals['installation cost']
        new = original.copy()
        new['depreciable'] = not original['depreciable']
        self.pf.set_params('installation cost',new)
        sol=self.pf.solve_price()
        self.pf.set_params('installation cost',original)
        assert sol['price'] == pytest.approx(self.hard_coded[63])

    def test_one_time_cap_inct_value(self):
        original = self.pf.vals['one time cap inct']
        new = original.copy()
        new['value'] = original['value']*1.5
        self.pf.set_params('one time cap inct',new)
        sol=self.pf.solve_price()
        self.pf.set_params('one time cap inct',original)
        assert sol['price'] == pytest.approx(self.hard_coded[64])

    def test_one_time_cap_inct_depr_type(self):
        original = self.pf.vals['one time cap inct']
        new = original.copy()
        new['depr type'] = 'MACRS' if original['depr type']=='Straight line' else 'Straight line'
        new['depr period'] = 7
        self.pf.set_params('one time cap inct',new)
        sol=self.pf.solve_price()
        self.pf.set_params('one time cap inct',original)
        assert sol['price'] == pytest.approx(self.hard_coded[65])

    def test_one_time_cap_inct_depreciable(self):
        original = self.pf.vals['one time cap inct']
        new = original.copy()
        new['depreciable'] = not original['depreciable']
        self.pf.set_params('one time cap inct',new)
        sol=self.pf.solve_price()
        self.pf.set_params('one time cap inct',original)
        assert sol['price'] == pytest.approx(self.hard_coded[66])

    def test_prop_tax_insurance(self):
        original = self.pf.vals['property tax and insurance']
        self.pf.set_params('property tax and insurance',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('property tax and insurance',original)
        assert sol['price'] == pytest.approx(self.hard_coded[67])

    def test_admin_expense(self):
        original = self.pf.vals['admin expense']
        self.pf.set_params('admin expense',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('admin expense',original)
        assert sol['price'] == pytest.approx(self.hard_coded[68])

    def test_tax_loss_carry_forward(self):
        original = self.pf.vals['tax loss carry forward years']
        self.pf.set_params('tax loss carry forward years',int(original*1.5))
        sol=self.pf.solve_price()
        self.pf.set_params('tax loss carry forward years',original)
        assert sol['price'] == pytest.approx(self.hard_coded[69])

    def test_capital_gains_tax_rate(self):
        original = self.pf.vals['capital gains tax rate']
        self.pf.set_params('capital gains tax rate',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('capital gains tax rate',original)
        assert sol['price'] == pytest.approx(self.hard_coded[70])

    def test_tax_losses_monetized(self):
        original = self.pf.vals['tax losses monetized']
        self.pf.set_params('tax losses monetized',not original)
        sol=self.pf.solve_price()
        self.pf.set_params('tax losses monetized',original)
        assert sol['price'] == pytest.approx(self.hard_coded[71])

    def test_sell_undepreciated_cap(self):
        original = self.pf.vals['sell undepreciated cap']
        self.pf.set_params('sell undepreciated cap',not original)
        sol=self.pf.solve_price()
        self.pf.set_params('sell undepreciated cap',original)
        assert sol['price'] == pytest.approx(self.hard_coded[72])

    def test_loan_period(self):
        original = self.pf.vals['loan period if used']
        self.pf.set_params('loan period if used',7)
        sol=self.pf.solve_price()
        self.pf.set_params('loan period if used',original)
        assert sol['price'] == pytest.approx(self.hard_coded[73])

    def test_debt_equity_ratio(self):
        original = self.pf.vals['debt equity ratio of initial financing']
        self.pf.set_params('debt equity ratio of initial financing',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('debt equity ratio of initial financing',original)
        assert sol['price'] == pytest.approx(self.hard_coded[74])

    def test_debt_interest(self):
        original = self.pf.vals['debt interest rate']
        self.pf.set_params('debt interest rate',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('debt interest rate',original)
        assert sol['price'] == pytest.approx(self.hard_coded[75])

    def test_debt_type(self):
        original = self.pf.vals['debt type']
        self.pf.set_params('debt type','Revolving debt' if original=='One time loan' else 'One time loan')
        sol=self.pf.solve_price()
        self.pf.set_params('debt type',original)
        assert sol['price'] == pytest.approx(self.hard_coded[76])

    def test_operating_incentives_taxable(self):
        original = self.pf.vals['annual operating incentive']
        adj = original.copy()
        adj['taxable'] = not original['taxable']
        self.pf.set_params('annual operating incentive',adj)
        sol=self.pf.solve_price()
        self.pf.set_params('annual operating incentive',original)
        assert sol['price'] == pytest.approx(self.hard_coded[43])

    def test_income_tax(self):
        original = self.pf.vals['total income tax rate']
        self.pf.set_params('total income tax rate',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('total income tax rate',original)
        assert sol['price'] == pytest.approx(self.hard_coded[77])

    def test_cash_onhand(self):
        original = self.pf.vals['cash onhand']
        self.pf.set_params('cash onhand',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('cash onhand',original)
        assert sol['price'] == pytest.approx(self.hard_coded[78])

    def test_inflation(self):
        original = self.pf.vals['general inflation rate']
        self.pf.set_params('general inflation rate',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('general inflation rate',original)
        assert sol['price'] == pytest.approx(self.hard_coded[79])

    def test_discount_rate(self):
        original = self.pf.vals['leverage after tax nominal discount rate']
        self.pf.set_params('leverage after tax nominal discount rate',original*1.5)
        sol=self.pf.solve_price()
        self.pf.set_params('leverage after tax nominal discount rate',original)
        assert sol['price'] == pytest.approx(self.hard_coded[80])

    
    