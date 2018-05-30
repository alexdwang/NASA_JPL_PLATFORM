import json
import GUI.FILEPATHS as FILEPATHS
import GUI.createNaLJson as NaLJson
import os
"""
' Library.py is used to load constant values from json files
' Contents in this file should not be modified by program unless you are updating the library
"""

PART_AD590 = NaLJson.PART_AD590
SIMULATION_MODEL = NaLJson.SIMULATION_MODEL
SIMULATION_SOURCE = NaLJson.SIMULATION_SOURCE
TPRE_RAD = NaLJson.TPRE_RAD
Input_Offset_Voltage = NaLJson.Input_Offset_Voltage
Input_Offset_Current = NaLJson.Input_Offset_Current
Positive_Input_Bias_Current = NaLJson.Positive_Input_Bias_Current
Negative_Input_Bias_Current = NaLJson.Negative_Input_Bias_Current
Nonlinearity = NaLJson.Nonlinearity
TEMPERATURE_5V = NaLJson.Temperature_5V
TEMPERATURE_ERROR_5V = NaLJson.Temperature_Error_5V
TEMPERATURE_30V = NaLJson.Temperature_30V
TEMPERATURE_ERROR_30V = NaLJson.Temperature_Error_30V
Load_Regulation = NaLJson.Load_Regulation

# os.chdir("/home/dwang/NASA_JPL/NASA_JPL_PLATFORM")
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
OUTPUT_NAME = name_json_dict['OUTPUT_NAME']
SIMULATION = name_json_dict['SIMULATION']
TID_LEVEL = name_json_dict['TID_LEVEL']
# EXCEL_FILE_PATH = name_json_dict['EXCEL_FILE_PATH']
COL_NAME = name_json_dict['COL_NAME']
# SHEET_NAME = name_json_dict['SHEET_NAME']
# NUM_OF_PARAMETER = name_json_dict['NUM_OF_PARAMETER']

# circuit code:
INPUT_VOLTAGE_SOURCE = library_json_dict['INPUT_VOLTAGE_SOURCE']
CIRCUIT_CORE = library_json_dict['CIRCUIT_CORE']
INPUT = library_json_dict['INPUT']
OUTPUT = library_json_dict['OUTPUT']
SUBCIRCUIT = library_json_dict['SUBCIRCUIT']
LIBRARY_TID_LEVEL_MODEL = library_json_dict['LIBRARY_TID_LEVEL_MODEL']
LIBRARY_JFET = library_json_dict['LIBRARY_JFET']

def save_name_to_json(TITLE, PARTS, SIMULATION, TID_LEVEL, TID_LIST, COL_NAME):
    output_object = {'TITLE': TITLE,
                     'PARTS': PARTS,
                     'SIMULATION': SIMULATION,
                     'TID_LEVEL': TID_LEVEL,
                     'TID_LIST': TID_LIST,
                     'COL_NAME': COL_NAME}
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