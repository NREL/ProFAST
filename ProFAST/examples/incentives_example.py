import ProFAST
import os

def setup_pf(h2s_size_days = 10):
    pf = ProFAST.ProFAST("central_grid_electrolysis_PEM")
    h2s_capex = 25.0 #[$/kg-H2]
    hydrogen_storage_capacity_kg = pf.vals['capacity']*h2s_size_days
    hydrogen_storage_capital_cost = hydrogen_storage_capacity_kg*h2s_capex

    pf.add_capital_item(
        "H2 Storage",
        hydrogen_storage_capital_cost,
        "MACRS",
        7,
        [0.],
    )

    return pf


def add_electrolyzer_itc(pf, pem_itc = 0.15):
    
    pem_itc = 0.15 # 15% ITC
    pem_capital_cost = pf.capital_items.get('Installed Capital',0).cost
    electrolyzer_itc_usd = pem_capital_cost*pem_itc
    pf.add_capital_incentive(
        'Electrolyzer ITC',
        electrolyzer_itc_usd,
        )
    return pf

def add_hydrogen_storage_itc(pf, h2s_itc = 0.30):
    h2s_itc = 0.3
    hydrogen_storage_capital_cost = pf.capital_items.get("H2 Storage",0).cost
    hydrogen_storage_itc_usd = hydrogen_storage_capital_cost*h2s_itc

    pf.add_capital_incentive(
        'H2 Storage ITC',
        hydrogen_storage_itc_usd,
        )
    return pf

if __name__ == "__main__":
    # --- NO ITC ---
    pf = setup_pf()
    sol = pf.solve_price()
    print(f"LCOH with no ITC: ${sol['price']:.2f}/kg")

    # --- ELECTROLYZER ITC ONLY ---
    pf = setup_pf()
    pf = add_electrolyzer_itc(pf)
    sol = pf.solve_price()
    print(f"LCOH with Electrolyzer ITC: ${sol['price']:.2f}/kg")

    # --- HYDROGEN STORAGE ITC ONLY ---
    pf = setup_pf()
    pf = add_hydrogen_storage_itc(pf)
    sol = pf.solve_price()
    print(f"LCOH with Hydrogen Storage ITC: ${sol['price']:.2f}/kg")

    # --- BOTH ITC ---
    pf = setup_pf()
    pf = add_hydrogen_storage_itc(pf)
    pf = add_electrolyzer_itc(pf)
    sol = pf.solve_price()
    print(f"LCOH with Electrolyzer and Hydrogen Storage ITC: ${sol['price']:.2f}/kg")