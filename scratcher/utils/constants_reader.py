import json

def constants_reader(key):
    with open('../config/constants.json', 'r') as json_file:
        constants = json.load(json_file)
        
    return constants[key]