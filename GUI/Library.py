import json
import GUI.FILEPATHS as FILEPATHS
import GUI.createNaLJson as NaLJson
import GUI.reset
"""
' Library.py is used to load constant values from json files
' Contents in this file should not be modified by program unless you are updating the library
"""

PART_AD590 = NaLJson.PART_AD590
PART_LT1175 = NaLJson.PART_LT1175
PART_LP2953 = NaLJson.PART_LP2953
PART_LM3940 = NaLJson.PART_LM3940

SIMULATION_MODEL = NaLJson.SIMULATION_MODEL
SIMULATION_SOURCE = NaLJson.SIMULATION_SOURCE
TPRE_RAD = NaLJson.TPRE_RAD
Input_Offset_Voltage = NaLJson.Input_Offset_Voltage
Input_Offset_Current = NaLJson.Input_Offset_Current
Positive_Input_Bias_Current = NaLJson.Positive_Input_Bias_Current
Negative_Input_Bias_Current = NaLJson.Negative_Input_Bias_Current
Nonlinearity = NaLJson.Nonlinearity
TEMPERATURE = NaLJson.Temperature
TEMPERATURE_ERROR = NaLJson.Temperature_Error
Load_Regulation = NaLJson.Load_Regulation

# os.chdir("/home/dwang/NASA_JPL/NASA_JPL_PLATFORM")
import_error = False
# read data from library
try:
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
    SPECIFICATION = specification_json_dict
except OSError as e:
    GUI.reset.do()
    import_error = True
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
    SPECIFICATION = specification_json_dict

# with open(FILEPATHS.SCALE_FILE_PATH, 'r') as f:
#     scale_jsonObject = f.readline()
# f.close()
# scale_json_dict = json.loads(scale_jsonObject)
# SCALELIB = scale_json_dict

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
EXTRA_LIBRARY = library_json_dict['EXTRA_LIBRARY']