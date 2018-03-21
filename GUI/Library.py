import json
import GUI.FILEPATHS as FILEPATHS

"""
' Library.py is used to load constant values from json files
' Contents in this file should not be modified by program unless you are updating the library
"""

SIMULATION_MODEL = 'compact model'
SIMULATION_SOURCE = 'external current source'
TPRE_RAD = 'pre_rad'

with open(FILEPATHS.NAME_FILE_PATH, 'r') as f:
    name_jsonObject = f.readline()
f.close()
name_json_dict = json.loads(name_jsonObject)

with open(FILEPATHS.LIBRARY_FILE_PATH, 'r') as f:
    library_jsonObject = f.readline()
f.close()
library_json_dict = json.loads(library_jsonObject)

with open(FILEPATHS.SPECIFICATION_FILE_PATH, 'r') as f:
    specification_jsonObject = f.readline()
f.close()
specification_json_dict = json.loads(specification_jsonObject)

with open(FILEPATHS.SCALE_FILE_PATH, 'r') as f:
    scale_jsonObject = f.readline()
f.close()
scale_json_dict = json.loads(scale_jsonObject)

SPECIFICATION = specification_json_dict
SCALELIB = scale_json_dict

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
OUTPUT = library_json_dict['OUTPUT']
OUTPUT_OPTION = library_json_dict['OUTPUT_OPTION']
SUBCIRCUIT = library_json_dict['SUBCIRCUIT']
LIBRARY_TID_LEVEL_MODEL = library_json_dict['LIBRARY_TID_LEVEL_MODEL']
LIBRARY_JFET = library_json_dict['LIBRARY_JFET']

def save_name_to_json(TITLE, PARTS, SIMULATION, TID_LEVEL, TID_LIST, EXCEL_FILE_PATH, COL_NAME, SHEET_NAME, NUM_OF_PARAMETER):
    output_object = {'TITLE': TITLE,
                     'PARTS': PARTS,
                     'SIMULATION': SIMULATION,
                     'TID_LEVEL': TID_LEVEL,
                     'TID_LIST': TID_LIST,
                     'EXCEL_FILE_PATH': EXCEL_FILE_PATH,
                     'COL_NAME': COL_NAME,
                     'SHEET_NAME': SHEET_NAME,
                     'NUM_OF_PARAMETER': NUM_OF_PARAMETER}
    with open(FILEPATHS.NAME_FILE_PATH, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return


def save_library_to_json(INPUT_VOLTAGE_SOURCE, CIRCUIT_CORE, SCALE, FUNCTIONS, INPUT, OUTPUT_OPTION, OUTPUT,
                         SUBCIRCUIT, LIBRARY_TID_LEVEL_MODEL, LIBRARY_JFET):
    output_object = {'INPUT_VOLTAGE_SOURCE': INPUT_VOLTAGE_SOURCE,
                     'CIRCUIT_CORE': CIRCUIT_CORE,
                     'SCALE': SCALE,
                     'FUNCTIONS': FUNCTIONS,
                     'INPUT': INPUT,
                     'OUTPUT': OUTPUT,
                     'OUTPUT_OPTION': OUTPUT_OPTION,
                     'SUBCIRCUIT': SUBCIRCUIT,
                     'LIBRARY_TID_LEVEL_MODEL': LIBRARY_TID_LEVEL_MODEL,
                     'LIBRARY_JFET': LIBRARY_JFET}

    with open(FILEPATHS.LIBRARY_FILE_PATH, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return