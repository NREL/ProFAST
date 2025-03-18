import ProFAST
import pytest

"""
Test that ProFAST returns outputs as expected
Author: Jared J. Thomas
"""

class TestSolution():
    pf = ProFAST.ProFAST('only_variables')
    sol = pf.solve_price()
    abs_tol = 1E-4

class TestInitial(TestSolution):
    def test_npv_zero(self):
        assert self.sol['NPV'] == pytest.approx(0, abs=self.abs_tol)
    
    def test_irr_zero(self):
        assert self.sol['irr'][1] == pytest.approx(self.pf.vals["leverage after tax nominal discount rate"] , abs=self.abs_tol)

    def test_wacc(self):
        
        assert self.sol['wacc'] == pytest.approx(0.0832112)

    def test_crf(self):
        
        assert self.sol['crf'] == pytest.approx(0.1042981)