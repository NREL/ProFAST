from importlib_resources import files
import json
import os
import numpy as np
from ProFAST import Pro_FAST
from ProFAST.tools.utilities import write_yaml, load_yaml
from ProFAST.tools import convert_pf_to_dict, populate_profast, make_price_breakdown, run_profast

class ProFastW(Pro_FAST):

    def __init__(self,case=None):
        super().__init__(case)
        self.one_time_capital_incentives = {}
        self.years_of_operation = []
    
    def make_price_breakdown(self):
        pf_config = self.export()
        sol, summary, cost_breakdown = run_profast(self)
        price_breakdown, lco_check = make_price_breakdown(cost_breakdown, pf_config)
        assert sol['price']==lco_check

        return price_breakdown
    
    def add_capital_incentive(self, name:str, value: float, **kwargs):
        valid_kwarg_keys = ["depr_type", "depr_period", "depreciable"]
        entry = {"value":value}

        if name in self.one_time_capital_incentives:
            raise ValueError(
                f"{name} capital incentive already exists. "
                "Please specify a different name or edit the incentive using pf.edit_capital_incentive()"
                )

        def type_check(name,value,types):
            if not isinstance(value,types):
                raise ValueError(f"Parameter: '{name}' cannot be of type {type(value)}. Type must be one of {types}")
        def check_in_list(name,value,list_vals):
            if value not in list_vals:
                raise ValueError(f"Parameter: '{name}' needs to be one of the following: {list_vals}")

        type_check('value',value,(int,np.floating,float))
        if bool(kwargs):
            invalid_keys = [k for k in kwargs.keys() if k not in valid_kwarg_keys]
            if len(invalid_keys)>0:
                msg = (
                    f"Invalid inputs {invalid_keys} provided. Valid inputs are {valid_kwarg_keys}."
                )
                raise ValueError(msg)
            
            if self.vals["one time cap inct"]["value"]>0:
                specified_keys = [k for k in valid_kwarg_keys if k in kwargs]
                mismatch_keys = [k for k in specified_keys if kwargs[k]!=self.vals["one time cap inct"][k]]
                if len(mismatch_keys)>0:
                    msg = (
                        f"{mismatch_keys} were given different values across the capital incentives. "
                        f"Please ensure that {valid_kwarg_keys} parameters are the same for all capital incentives."
                        f"Update capital incentive parameters using pf.vals['one time cap inct'][param]=val"
                    )
                    raise ValueError(msg)
            
            depr_type = self.vals['one time cap inct'].get('depr type',"MACRS")

            if 'depr_type' in kwargs:
                type_check('depr_type',kwargs['depr_type'], str)
                check_in_list('depr_type',kwargs['depr type'], ["MACRS", "Straight line"])
                
                self.vals['one time cap inct'].update({'depr type':kwargs['depr_type']})

                depr_type = kwargs.get('depr type','MACRS')

            if 'depr_period' in kwargs:
                type_check('depr_period',kwargs['depr_period'], int)
                if depr_type=='MACRS':
                    check_in_list('depr_period',kwargs['depr_period'], [3, 5, 7, 10, 15, 20])
                self.vals['one time cap inct'].update({'depr period':kwargs['depr_period']})
            
            if 'depreciable' in kwargs:
                type_check('depreciable',kwargs['depreciable'],bool)
                self.vals['one time cap inct'].update({'depreciable':kwargs['depreciable']})

            entry.update(kwargs)
            
        self.one_time_capital_incentives[name] = entry
        itc_tot = self.vals['one time cap inct']['value'] + value
        self.vals['one time cap inct'].update({'value':itc_tot})
        
    
    def edit_capital_incentive(self,name: str, value: dict):
        for key, val in value.items():
            if key not in ["value","depr_type", "depr_period", "depr type", "depr period", "depreciable"]:  # Check if it is a valid value
                raise Exception(f"{key} is not a valid value to edit!")
            if name not in self.one_time_capital_incentives:  # Check if the incentive name exists
                raise Exception(f"{name} does not exist!")
            
            self.one_time_capital_incentives[name].update({key.replace("_"," "):val})
            
        
        itc_vals = [v['value'] for k,v in self.one_time_capital_incentives.items()]
        self.vals['one time cap inct'].update({'value':sum(itc_vals)})
    
    def remove_capital_incentive(self, name):
        removed_incentive = self.one_time_capital_incentives.pop(name)

        itc_vals = [v['value'] for k,v in self.one_time_capital_incentives.items()]
        self.vals['one time cap inct'].update({'value':sum(itc_vals)})

    def load_json(self,case=""):
        self.clear_values("all")
        if os.path.isfile(case):
            f = open(case)
        elif os.path.isfile(files("ProFAST.resources").joinpath(f"{case}.json")):
            f = open(files("ProFAST.resources").joinpath(f"{case}.json"))
        else:
            raise ValueError(f'File location "{case}.json" not found')
        # f = open(f'{self.__location__}/../resources/{case}.json')
        data = json.load(f)
        json_key_mapper = {
            "variables":"params",
            "capital item": "capital_items",
            "fixed cost": "fixed_costs",
            "feedstock": "feedstocks",
            "coproduct": "coproducts",
            "incentive":"incentives"
            }
        # pf_config = {json_key_mapper[k]:v for k,v in data.items()}
        pf_config = {}
        for entry_type, entry_items in data.items():
            if isinstance(entry_items,list):
                entries = {}
                for eitem in entry_items:
                    name = eitem.pop("name")
                    entries[name] = eitem
                pf_config[json_key_mapper[entry_type]] = entries
            else:
                pf_config[json_key_mapper[entry_type]] = entry_items

        populate_profast(pf_config,self)
        

    def load_yaml(self, filepath):
        input_params = load_yaml(filepath)
        populate_profast(input_params,self)
    
    def export(self):
        pf_dict = convert_pf_to_dict(self)
        return pf_dict
    
    def to_yaml(self,filepath):
        pf_dict = convert_pf_to_dict(self)
        write_yaml(filepath,pf_dict)

    def calculate_years_of_operation(self):
        operation_start_year = self.vals['analysis start year'] + (self.vals['installation months'] / 12)
        if self.vals['operating life']>1:
            self.years_of_operation = np.arange(
                int(operation_start_year), int(operation_start_year + self.vals['operating life']), 1
            ).tolist()
        else:
            self.years_of_operation=[int(operation_start_year)]

    # @property
    # def vals(self):
    #     return self.vals
    
    # @vals.setter
    # def vals(self, name:str, value):
    #     self.set_params(name,value)
        
    #     if name in ["analysis start year","installation months","operating life"]:
    #         self.calculate_years_of_operation()

    # @ProFAST.vals.setter
    # def vals(self, name:str, value):

    # @property
    # def params(self):
    #     return self.vals

    # @params.setter
    # def params(self, name:str, value):
    #     if name == "one time cap inct":
    #         if isinstance(value,dict):
    #             itc_tot = self.vals['one time cap inct']['value'] + value['value']
    #             itc_dict = {k:v for k,v in value.items() if k!='value'}
    #             itc_dict['value'] = itc_tot
    #             self.set_params('one time cap inct',itc_dict)
    #             return 
    #         if isinstance(value,(int,float,np.floating)):
    #             itc_tot = self.vals['one time cap inct']['value'] + value['value']
    #             itc_dict = {k:v for k,v in self.vals['one time cap inct'].items() if k!='value'}
    #             itc_dict['value'] = itc_tot
    #             self.set_params('one time cap inct',itc_dict)
    #             return
    #         raise ValueError(f"{name} must either be numeric value or dictionary.")

    #     else:
    #         self.set_params(name,value)


# if __name__ == "__main__":
#     pfw = ProFastW()
#     pfw.set_params("commodity",{"name": "temp","unit":"kg","initial price": 100, "escalation": 0.0})
#     pfw.add_capital_incentive("test1",100)
#     pfw.add_capital_incentive("test2",200)
#     []