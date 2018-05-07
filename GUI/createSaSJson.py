import json

import GUI.FILEPATHS as FILEPATHS
import GUI.createNaLJson as createNaLJson

'''
'   create specification.json and scale.json
'''
def save_specification_to_json(SPECIFICATION):
    output_object = SPECIFICATION
    with open("../" + FILEPATHS.SPECIFICATION_FILE_PATH, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return


def save_scale_to_json(Scale):
    output_object = Scale
    with open("../" + FILEPATHS.SCALE_FILE_PATH, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return

# SPECIFICATION = {PART_NAME: {OUTPUT_NAME: [MIN, MAX]}}
SPECIFICATION = {createNaLJson.PART_AD590: {createNaLJson.Nonlinearity: [-1,1],
                                            createNaLJson.Temperature: [20, 30],
                                            createNaLJson.Temperature_Error: [-5, 5],
                                            "Dataset": [30]},

                 createNaLJson.PART_LT1175: {createNaLJson.Line_Regulation: [0, 0.015],
                                             createNaLJson.Output_Voltage: [4.93, 5.075],
                                             createNaLJson.Dropoff_Voltage: [0, 0.7],
                                             createNaLJson.Load_Regulation: [0, 0.35],      # Line Regulation
                                            "Dataset": [-20]},

                 createNaLJson.PART_TL431: {createNaLJson.Reference_Voltage: [2.44, 2.55],   # Vref
                                            createNaLJson.Reference_Input_Current: [-4e-6, 4e-6],       # Iref
                                            createNaLJson.Cathode_Current_Ika: [-1e-6, 1e-6],       # Ika
                                            createNaLJson.Cathode_Voltage_Vka: [None, None],
                                            createNaLJson.Ratio_DVref_DVka: [0, -2.7],       # Vka
                                            "Dataset": [25]
                                            },
                 createNaLJson.PART_LM111: {createNaLJson.Supply_Current: [0, 6e-3],
                                            # createNaLJson.Supply_Current: [-5e-6, 0],
                                            createNaLJson.Input_Offset_Voltage: [-10e-9, 10e-9],
                                            createNaLJson.Input_Offset_Current: [-3e-6, 3e-6],
                                            createNaLJson.Positive_Input_Bias_Current: [-150e-9, 0.1e-9],
                                            createNaLJson.Negative_Input_Bias_Current: [-150e-9, 0.1e-9],
                                            "Dataset": [15]},
                 createNaLJson.PART_LM193: {createNaLJson.Supply_Current: [0, 3e-3],      # Supply Current
                                            createNaLJson.Input_Offset_Voltage: [-5e-3, 5e-3],      # Input Offset Voltage
                                            createNaLJson.Positive_Input_Bias_Current: [-100e-9, 100e-9],      # Positive Input Bias Current
                                            createNaLJson.Negative_Input_Bias_Current: [-100e-9, 100e-9],      # Negative Input Bias Current
                                            createNaLJson.Input_Offset_Current: [-25e-9, 25e-9],               # Input Offset Current
                                            "Dataset": [30]},
                 createNaLJson.PART_LT1006: {createNaLJson.Supply_Current: [-0.1e-6, 599.9e-6],
                                             createNaLJson.Input_Offset_Voltage: [-180e-6, 180e-6],
                                             createNaLJson.Input_Offset_Current: [-0.9e-9, 0.9e-9],
                                             createNaLJson.Positive_Input_Bias_Current: [-20e-9, 20e-9],
                                             createNaLJson.Negative_Input_Bias_Current: [-20e-9, 20e-9],
                                            "Dataset": [5]},
                 createNaLJson.PART_LP2953: {createNaLJson.Output_Voltage: [4.93, 5.07],
                                             createNaLJson.Reference_Voltage: [1.215, 1.245],
                                            "Dataset": [0.25]},
                 createNaLJson.PART_LM3940: {createNaLJson.Supply_Current: [0, 1.7],
                                             createNaLJson.Output_Voltage: [3.2, 3.4],
                                            "Dataset": [5]}
                 }

save_specification_to_json(SPECIFICATION)

SCALE = {createNaLJson.PART_TL431: {'scale': [2, 3, 2, 1, 1, 7.2, 0.9, 1, 1, 2.5, 50],
                                    'type': ['NPN', 'NPN', 'PNP', 'PNP', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN']}}
save_scale_to_json(SCALE)