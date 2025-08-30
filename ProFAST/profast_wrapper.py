from importlib_resources import files
import json
import os
import numpy as np
from ProFAST import Pro_FAST
from ProFAST.tools.utilities import write_yaml, load_yaml, rename_dict_keys
from ProFAST.tools import convert_pf_to_dict, populate_profast, make_price_breakdown, run_profast
import matplotlib.pyplot as plt
import matplotlib as mpl

class ProFastW(Pro_FAST):

    def __init__(self,case=None):
        if case is not None:
            if ".yaml" in case:
                super().__init__(None)
                self.load_yaml(case)
            else:
                super().__init__(case)
        else: 
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
        if ".json" in case:
            case = case.replace(".json","")
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
        
        pf_config = {}
        for entry_type, entry_items in data.items():
            if isinstance(entry_items,list):
                entries = {}
                for eitem in entry_items:
                    name = eitem.pop("name")
                    eitem = rename_dict_keys(eitem,"depr period","depr_period")
                    eitem = rename_dict_keys(eitem,"depr type","depr_type")
                    entries[name] = eitem
                pf_config[json_key_mapper[entry_type]] = entries
            elif isinstance(entry_items,dict):
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

    def plot_price_breakdown(self,fileout="", show_plot=True):
        price_breakdown = self.make_price_breakdown()
        lco_str = "LCO{}".format(self.vals["commodity"]["name"][0])
        lco_units = "$/{}".format(self.vals["commodity"]["unit"])
        lco_total = price_breakdown.pop(f"{lco_str}: Total ({lco_units})")
        
        if len(price_breakdown)<=10:
            colors = mpl.colormaps['tab10'].colors
        elif len(price_breakdown)>10 and len(price_breakdown)<=20:
            colors = mpl.colormaps['tab20'].colors
        elif len(price_breakdown)>20:
            colors = mpl.colormaps['turbo'](np.linspace(0,1,len(price_breakdown)))
        
        price_items = [k for k,v in price_breakdown.items() if v>0]
        longest_string = max([len(k) for k in price_items])
        min_val = min([price_breakdown[k] for k in price_items])
        fs = 10
        min_text_width = longest_string*fs/72
        min_text_height = min([10,int(np.ceil((lco_total/min_val)*fs/72))])

        fig, ax = plt.subplots(figsize=(int(np.ceil(min_text_width)), min_text_height))
        if not hasattr(ax, 'side_label_count'):
            ax.side_label_count = 0
        start_val = 0
        bw = 5.0
        x_val = 5.0
        for item,bar_color in zip(price_items,colors):
            item_label = item.replace(lco_str,"").replace(lco_units,"").strip("(): ")
            # label_with_val = f"{lco_str} {item_label}: {price_breakdown[item]:.3f} ({lco_units})"
            label_with_val = f"{item_label}: {price_breakdown[item]:.3f} ({lco_units})"
            p1 = ax.bar(
                        x_val,
                        price_breakdown[item],
                        width=bw,
                        label=item_label,
                        bottom=start_val,
                        alpha=0.5,
                        color=bar_color,
                    )
            if (price_breakdown[item]*10/lco_total)<0.25:
                
                bar_mid = start_val + price_breakdown[item]/2
                
                ax.annotate(
                    label_with_val,
                    xy=(7.5,bar_mid),
                    xytext=(7.5,bar_mid+0.1*ax.side_label_count),
                    xycoords='data',
                    arrowprops=dict(arrowstyle="->", lw=1, alpha=0.3),
                    va='center',
                    ha='left',
                    color=bar_color
                    )
                
                ax.side_label_count += 1
            else:
                ax.bar_label(
                    p1,
                    labels=[label_with_val],
                    label_type="center",
                    fontsize = fs,
                )
                ax.side_label_count = 0

            start_val += price_breakdown[item]
        ax.set_ylabel(f"Levelized cost of {self.vals['commodity']['name']} ({lco_str} in {lco_units})",fontsize=fs)
        ax.set_xticks(ticks=[x_val], labels=[''])
        txt = ax.annotate(
                f"{lco_str} {lco_total:.3f} {lco_units}",
                xy=(x_val, lco_total),
                xycoords='data',
                horizontalalignment="center",
                verticalalignment="bottom",
                fontweight="bold",
                fontsize = fs,
            )
        ax.spines[['right', 'top']].set_visible(False)
        if fileout != "":
            fig.savefig(fileout,bbox_inches='tight')
        if show_plot:
            plt.show()
        else:
            plt.close()


        []
   