import os
import yaml

class Loader(yaml.SafeLoader):

    def __init__(self, stream):

        self._root = os.path.split(stream.name)[0]

        super().__init__(stream)

    def include(self, node):

        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, self.__class__)


Loader.add_constructor('!include', Loader.include)

def load_yaml(filename, loader=Loader) -> dict:
    if isinstance(filename, dict):
        return filename  # filename already yaml dict
    with open(filename) as fid:
        return yaml.load(fid, loader)

def write_yaml(filename,data):
    if not '.yaml' in filename:
        filename = filename +'.yaml'

    with open(filename, 'w+') as file:
        yaml.dump(data, file,sort_keys=False,encoding = None,default_flow_style=False)

def update_keyname(orig_dict, init_key, new_keyname):

    for key, val in orig_dict.copy().items():
        if isinstance(val, dict):
            tmp = update_keyname(orig_dict.get(key, {}), init_key, new_keyname)
            orig_dict[key] = tmp
        else:
            if isinstance(key, list):
                for i, k in enumerate(key):
                    if k == init_key:
                        orig_dict.update({new_keyname:orig_dict.get(k)})
                    else:
                        orig_dict[k] = orig_dict.get(key, []) + val[i]
            elif isinstance(key, str):
                if key == init_key:
                    orig_dict.update({new_keyname:orig_dict.get(key)})
    return orig_dict

def remove_keynames(orig_dict, init_key):

    for key, val in orig_dict.copy().items():
        if isinstance(val, dict):
            tmp = remove_keynames(orig_dict.get(key, {}), init_key)
            orig_dict[key] = tmp
        else:
            if isinstance(key, list):
                for i, k in enumerate(key):
                    if k == init_key:
                        orig_dict.pop(k)
                    else:
                        orig_dict[k] = orig_dict.get(key, []) + val[i]
            elif isinstance(key, str):
                if key == init_key:
                    orig_dict.pop(key)
    return orig_dict

def rename_dict_keys(input_dict,init_keyname,new_keyname):
    input_dict = update_keyname(input_dict,init_keyname,new_keyname)
    input_dict = remove_keynames(input_dict,init_keyname)
    return input_dict
    