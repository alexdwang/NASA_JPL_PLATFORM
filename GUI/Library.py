import json

"""
' Library.py is used to load constant values from json files
' Contents in this file should not be modified by program unless you are updating the library
"""

SIMULATION_MODEL = 'model'
SIMULATION_SOURCE = 'source'
TPRE_RAD = 'pre_rad'

with open("Library/name.json", 'r') as f:
    name_jsonObject = f.readline()
f.close()
name_json_dict = json.loads(name_jsonObject)

with open("Library/library.json", 'r') as f:
    library_jsonObject = f.readline()
f.close()
library_json_dict = json.loads(library_jsonObject)

TITLE = name_json_dict['TITLE']
PARTS = name_json_dict['PARTS']
SIMULATION = name_json_dict['SIMULATION']
TID_LEVEL = name_json_dict['TID_LEVEL']
TID_LIST = name_json_dict['TID_LIST']
EXCEL_FILE_PATH = name_json_dict['EXCEL_FILE_PATH']
COL_NAME = name_json_dict['COL_NAME']
SHEET_NAME = name_json_dict['SHEET_NAME']
NUM_OF_PARAMETER = name_json_dict['NUM_OF_PARAMETER']

# circuit code:
INPUT_VOLTAGE_SOURCE = library_json_dict['INPUT_VOLTAGE_SOURCE']
CIRCUIT_CORE = library_json_dict['CIRCUIT_CORE']
SCALE = library_json_dict['SCALE']
FUNCTIONS = library_json_dict['FUNCTIONS']
INPUT = library_json_dict['INPUT']
OUTPUT_OPTION = library_json_dict['OUTPUT_OPTION']
OUTPUT = library_json_dict['OUTPUT']
SUBCIRCUIT = library_json_dict['SUBCIRCUIT']
LIBRARY_TID_LEVEL_MODEL = library_json_dict['LIBRARY_TID_LEVEL_MODEL']
LIBRARY_JFET = library_json_dict['LIBRARY_JFET']