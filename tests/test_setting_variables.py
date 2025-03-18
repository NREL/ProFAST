import ProFAST
import pytest

class TestSettingVariables():
    pf = ProFAST.ProFAST('only_variables')

class TestCapacity(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('capacity','5000')
    def test_neg(self):
        with pytest.raises(ValueError):
            self.pf.set_params('capacity',-1)

class TestNonDeprAssets(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('non depr assets','5000')
    def test_neg(self):
        with pytest.raises(ValueError):
            self.pf.set_params('non depr assets',-1)

class TestNonDeprAssetsSale(TestSettingVariables):           
    def test_non_depr_asset_sale_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('nend of proj sale non depr assets','5000')
    def test_non_depr_asset_sale_neg(self):
        with pytest.raises(ValueError):
            self.pf.set_params('end of proj sale non depr assets',-1)

class TestDemandRampup(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('demand rampup','5000')
    def test_neg(self):
        with pytest.raises(ValueError):
            self.pf.set_params('demand rampup',-1)

class TestUtil(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('long term utilization','5000')

class TestCCFees(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('credit card fees','5000')

class TestSalesTax(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('sales tax','5000')

class TestPropTaxIns(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('property tax and insurance','5000')

class TestAdminExpense(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('admin expense','5000')

class TestTaxRate(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('total income tax rate','5000')

class TestCapitalGains(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('capital gains tax rate','5000')

class TestInflation(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('general inflation rate','5000')

class TestDiscountRate(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('leverage after tax nominal discount rate','5000')

class TestDebtEquityRatio(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('debt equity ratio of initial financing','5000')

class TestDebtInterest(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('debt interest rate','5000')

class TestCashOnHand(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('cash onhand','5000')

class TestInstallCost(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation cost','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation cost',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation cost',{'value':'a','depr type':'MACRS','depr period':5,'depreciable':True})
    def test_depr_type(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation cost',{'value':1,'depr type':'MACRS_ERROR','depr period':5,'depreciable':True})
    def test_depr_period(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation cost',{'value':1,'depr type':'Straight line','depr period':-1,'depreciable':True})
    def test_MACRS_period(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation cost',{'value':1,'depr type':'MACRS','depr period':2,'depreciable':True})
    def test_depreciable(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation cost',{'value':1,'depr type':'MACRS','depr period':5,'depreciable':'True'})

class TestOneTimeCapInt(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('one time cap inct','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('one time cap inct',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('one time cap inct',{'value':'a','depr type':'MACRS','depr period':5,'depreciable':True})
    def test_depr_type(self):
        with pytest.raises(ValueError):
            self.pf.set_params('one time cap inct',{'value':1,'depr type':'MACRS_ERROR','depr period':5,'depreciable':True})
    def test_depr_period(self):
        with pytest.raises(ValueError):
            self.pf.set_params('one time cap inct',{'value':1,'depr type':'Straight line','depr period':-1,'depreciable':True})
    def test_MACRS_period(self):
        with pytest.raises(ValueError):
            self.pf.set_params('one time cap inct',{'value':1,'depr type':'MACRS','depr period':2,'depreciable':True})
    def test_depreciable(self):
        with pytest.raises(ValueError):
            self.pf.set_params('one time cap inct',{'value':1,'depr type':'MACRS','depr period':5,'depreciable':'True'})
    
class TestMaintenance(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('maintenance','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('maintenance',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('maintenance',{'value':'a','escalation':0.1})
    def test_escalation(self):
        with pytest.raises(ValueError):
            self.pf.set_params('maintenance',{'value':1,'escalation':'a'})

class TestIncidentalRevenue(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('incidental revenue','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('incidental revenue',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('incidental revenue',{'value':'a','escalation':0.1})
    def test_escalation(self):
        with pytest.raises(ValueError):
            self.pf.set_params('incidental revenue',{'value':1,'escalation':'a'})

class TestLicenseAndPermit(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('license and permit','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('license and permit',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('license and permit',{'value':'a','escalation':0.1})
    def test_escalation(self):
        with pytest.raises(ValueError):
            self.pf.set_params('license and permit',{'value':1,'escalation':'a'})

class TestRent(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('rent','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('rent',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('rent',{'value':'a','escalation':0.1})
    def test_escalation(self):
        with pytest.raises(ValueError):
            self.pf.set_params('rent',{'value':1,'escalation':'a'})

class TestRoadTax(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('road tax','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('road tax',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('road tax',{'value':'a','escalation':0.1})
    def test_escalation(self):
        with pytest.raises(ValueError):
            self.pf.set_params('road tax',{'value':1,'escalation':'a'})

class TestLabor(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('labor','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('labor',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('labor',{'value':'a','rate':1,'escalation':0.1})
    def test_rate(self):
        with pytest.raises(ValueError):
            self.pf.set_params('labor',{'value':1,'rate':'a','escalation':0.1})
    def test_escalation(self):
        with pytest.raises(ValueError):
            self.pf.set_params('labor',{'value':1,'rate':1,'escalation':'a'})

class TestAnalysisStartYear(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('analysis start year', '5000')
    def test_float(self):
        with pytest.raises(ValueError):
            self.pf.set_params('analysis start year', float(2030.0))
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('analysis start year', -1)

class TestOperatingLife(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('operating life','5000')
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('aoperating life',-1)

class TestInstallationMonths(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation months','5000')
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('installation months',-1)
    
class TestTaxLossCarryForward(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('tax loss carry forward years','5000')
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('tax loss carry forward years',-1)

class TestLoanPeriod(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('loan period if used','5000')
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('loan period if used',-1)

class TestSellUndeprCap(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('sell undepreciated cap','5000')

class TestTaxLossMonetize(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('tax losses monetized','5000')

class TestAnnulOperatingIncentive(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('annual operating incentive','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('annual operating incentive',{'value':1,'lorem':'ipsum'})
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('annual operating incentive',{'value':'a','decay':1,'sunset years':1,'taxable':True})
    def test_decay(self):
        with pytest.raises(ValueError):
            self.pf.set_params('annual operating incentive',{'value':1,'decay':'1','sunset years':1,'taxable':True})
    def test_sunset_years(self):
        with pytest.raises(ValueError):
            self.pf.set_params('annual operating incentive',{'value':1,'decay':1,'sunset years':'1','taxable':True})
    def test_taxable(self):
        with pytest.raises(ValueError):
            self.pf.set_params('annual operating incentive',{'value':1,'decay':1,'sunset years':1,'taxable':'True'})

class TestTOPC(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('TOPC','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('TOPC',{'value':1,'lorem':'ipsum'})
    def test_unit_price(self):
        with pytest.raises(ValueError):
            self.pf.set_params('TOPC',{'unit price':'1','decay':1,'support utilization':0.1,'sunset years':1})
    def test_decay(self):
        with pytest.raises(ValueError):
            self.pf.set_params('TOPC',{'unit price':1,'decay':'1','support utilization':0.1,'sunset years':1})
    def test_support_utilization(self):
        with pytest.raises(ValueError):
            self.pf.set_params('TOPC',{'unit price':1,'decay':1,'support utilization':'0.1','sunset years':1})
    def test_sunset_years(self):
        with pytest.raises(ValueError):
            self.pf.set_params('TOPC',{'unit price':1,'decay':1,'support utilization':0.1,'sunset years':'1'})

class TestDebtType(TestSettingVariables):
    def test_value(self):
        with pytest.raises(ValueError):
            self.pf.set_params('debt type','Cash')

class TestCommodity(TestSettingVariables):
    def test_str(self):
        with pytest.raises(ValueError):
            self.pf.set_params('commodity','5000')
    def test_key_vals(self):
        with pytest.raises(ValueError):
            self.pf.set_params('commodity',{'value':1,'lorem':'ipsum'})
    def test_unit_price(self):
        with pytest.raises(ValueError):
            self.pf.set_params('commodity',{'name':1,'initial price':1,'unit':'ipsum','escalation':0.1})
    # def test_initial_price(self):
    #     with pytest.raises(ValueError):
    #         self.pf.set_params('commodity',{'name':'lorem','initial price':'1','unit':'ipsum','escalation':0.1})
    def test_unit(self):
        with pytest.raises(ValueError):
            self.pf.set_params('commodity',{'name':'lorem','initial price':1,'unit':1,'escalation':0.1})
    def test_escalation(self):
        with pytest.raises(ValueError):
            self.pf.set_params('commodity',{'name':'lorem','initial price':1,'unit':'ipsum','escalation':'0.1'})