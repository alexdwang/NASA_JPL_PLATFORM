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

# SPECIFICATION = {PART_NAME: {OUTPUT_NAME: [MIN, MAX, UNIT]}}
SPECIFICATION = {createNaLJson.PART_AD590: {createNaLJson.Nonlinearity: [-1,1, 'C'],
                                            createNaLJson.Temperature_5V: [20, 30, 'C'],
                                            createNaLJson.Temperature_Error_5V: [-5, 5,'C'],
                                            createNaLJson.Temperature_30V: [20, 30, 'C'],
                                            createNaLJson.Temperature_Error_30V: [-5, 5, 'C'],
                                            "Dataset": [5, 30]},

                 createNaLJson.PART_LT1175: {createNaLJson.Line_Regulation: [0, 0.015,'%/V'],
                                             createNaLJson.Output_Voltage: [-5.075,-4.93, 'V'],
                                             createNaLJson.Dropoff_Voltage: [0, 0.7,'V'],
                                             createNaLJson.Load_Regulation: [0, 0.35,'%'],
                                             createNaLJson.Sense_Current: [None, None, 'A'],
                                            "Dataset": [-20, 0]},

                 createNaLJson.PART_TL431: {createNaLJson.Reference_Voltage: [2.44, 2.55,'V'],   # Vref
                                            createNaLJson.Reference_Input_Current: [-4e-6, 4e-6,'A'],       # Iref
                                            createNaLJson.Cathode_Current_Ika: [-1e-6, 1e-6,'A'],       # Ika
                                            createNaLJson.Cathode_Voltage_Vka: [None, None,'V'],
                                            createNaLJson.Ratio_DVref_DVka: [0, -2.7, 'mV/V'],       # Vka
                                            "Dataset": [25]
                                            },
                 createNaLJson.PART_LM111: {createNaLJson.Supply_Current: [0, 6e-3,'A'],
                                            # createNaLJson.Supply_Current: [-5e-6, 0],
                                            createNaLJson.Input_Offset_Voltage: [-3e-3, 3e-3,'V'],
                                            createNaLJson.Input_Offset_Current: [-1e-8, 1e-8,'A'],
                                            createNaLJson.Positive_Input_Bias_Current: [-1e-7, 1e-10,'A'],
                                            createNaLJson.Negative_Input_Bias_Current: [-1e-7, 1e-10,'A'],
                                            "Dataset": [15]},
                 createNaLJson.PART_LM193: {createNaLJson.Supply_Current: [0, 3e-3,'A'],      # Supply Current
                                            createNaLJson.Input_Offset_Voltage: [-5e-3, 5e-3,'V'],      # Input Offset Voltage
                                            createNaLJson.Positive_Input_Bias_Current: [-100e-9, 100e-9,'A'],      # Positive Input Bias Current
                                            createNaLJson.Negative_Input_Bias_Current: [-100e-9, 100e-9,'A'],      # Negative Input Bias Current
                                            createNaLJson.Input_Offset_Current: [-25e-9, 25e-9,'A'],               # Input Offset Current
                                            "Dataset": [30]},
                 createNaLJson.PART_LT1006: {createNaLJson.Supply_Current: [-0.1e-6, 599.9e-6,'A'],
                                             createNaLJson.Input_Offset_Voltage: [-180e-6, 180e-6,'V'],
                                             createNaLJson.Input_Offset_Current: [-0.9e-9, 0.9e-9,'A'],
                                             createNaLJson.Positive_Input_Bias_Current: [-20e-9, 20e-9,'A'],
                                             createNaLJson.Negative_Input_Bias_Current: [-20e-9, 20e-9,'A'],
                                            "Dataset": [5]},
                 createNaLJson.PART_LP2953: {createNaLJson.Output_Voltage_With_Vin_6V: [4.93, 5.07,'V'],
                                             createNaLJson.Output_Voltage_With_Vin_23V: [4.93, 5.07,'V'],
                                             createNaLJson.Output_Voltage_With_Vin_30V: [4.93, 5.07,'V'],
                                             createNaLJson.Reference_Voltage_With_Vin_6V: [1.215, 1.245,'V'],
                                             createNaLJson.Reference_Voltage_With_Vin_23V: [1.215, 1.245,'V'],
                                             createNaLJson.Reference_Voltage_With_Vin_30V: [1.215, 1.245,'V'],
                                            "Dataset": [0]},
                 createNaLJson.PART_LM3940: {createNaLJson.Supply_Current: [0, 1.7,'A'],
                                             createNaLJson.Output_Voltage: [3.2, 3.4,'V'],
                                             createNaLJson.Reference_Voltage: [1.215, 1.245, 'V'],
                                            "Dataset": [0]}
                 }

save_specification_to_json(SPECIFICATION)
#
# SCALE = {createNaLJson.PART_TL431: {'scale': [2, 3, 2, 1, 1, 7.2, 0.9, 1, 1, 2.5, 50],
#                                     'type': ['NPN', 'NPN', 'PNP', 'PNP', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN']}}
# save_scale_to_json(SCALE)