import json
import re
import GUI.FILEPATHS as FILEPATHS
import GUI.createNaLJson as createNaLJson

'''
'   create specification.json and scale.json
'''

def save():
    save_specification_to_json(SPECIFICATION, path=FILEPATHS.SPECIFICATION_FILE_PATH)

def save_specification_to_json(SPECIFICATION, path="../" + FILEPATHS.SPECIFICATION_FILE_PATH):
    output_object = SPECIFICATION
    with open(path, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return


def save_scale_to_json(Scale, path="../" + FILEPATHS.SCALE_FILE_PATH):
    output_object = Scale
    with open(path, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return



def save_txt_to_specfication(path="../" + FILEPATHS.SPEC_TXT_FILE_PATH):
    SPEC = {}
    is_the_right_file = 0
    part_name = ''
    properity_name = ''
    data_set = []
    #min_limit = None
    #max_limit = None
    i = 0
    with open(path, "r") as f:
        for line in f.readlines():

            #print(line.strip())
            #print(re.match(r'\*+', line))

            if re.match(r'\*+\n', line):
                i = i+1
                #print(line.strip())
            elif re.match(r'\*Specification\*\n', line):
                i = i+1
                #print(line.strip())
            elif re.match(r'\*.+\*\n', line):
                temp = line.strip()
                temp = temp.strip('*')
                part_name = temp
                SPEC[temp] = {}
                #print("part name: ", temp)
            elif re.match(r'Dataset=.+', line):
                temp = line.strip()
                equal = temp.find('=')
                data_set = temp[equal+1:].split(',')
                results = list(map(int, data_set))
                SPEC[part_name]['Dataset'] = results

                #print("DATASET: ", temp[equal+1:])


            elif re.match(r'\*.+\n', line):

                last = line.find('(')
                temp = line[1:last].strip()
                properity_name = temp
                SPEC[part_name][properity_name] = []
                #print("properity: ", line[1:last])
            elif re.match(r'min=.+\n', line):
                first = line.find('=')
                try:
                    min_limit = int(line[first+1:])
                except ValueError:
                    min_limit = float(line[first + 1:])
                #min_limit = float(line[first+1:])
                SPEC[part_name][properity_name].append(min_limit)
                #print("MIN: ", line[first+1:].strip())
            elif re.match(r'max=.+\n', line):
                first = line.find('=')
                try:
                    max_limit = int(line[first+1:])
                except ValueError:
                    max_limit = float(line[first + 1:])
                #max_limit = float(line[first + 1:])
                SPEC[part_name][properity_name].append(max_limit)
                #print("MAX: ", line[first+1:].strip())
            elif re.match(r'unit=.+\n', line):
                first = line.find('=')
                unit = line[first + 1:].strip()
                SPEC[part_name][properity_name].append(unit)

                data_temp = SPEC[part_name]['Dataset']
                SPEC[part_name].pop('Dataset')
                SPEC[part_name]['Dataset'] = data_temp

                #print("UNIT: ", line[first+1:].strip())
    f.close()
    #print(SPEC)
    return SPEC


# SPECIFICATION = {PART_NAME: {OUTPUT_NAME: [MIN, MAX, UNIT]}}
SPECIFICATION = {createNaLJson.PART_AD590: {createNaLJson.Nonlinearity: [-1,1, 'C'],
                                            createNaLJson.Temperature: [20, 30, 'C'],
                                            createNaLJson.Temperature_Error: [-5, 5,'C'],
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

if __name__=='__main__':

    # s = save_txt_to_specfication()
    # save_specification_to_json(s)

    save_specification_to_json(SPECIFICATION)
    #
    # SCALE = {createNaLJson.PART_TL431: {'scale': [2, 3, 2, 1, 1, 7.2, 0.9, 1, 1, 2.5, 50],
    #                                     'type': ['NPN', 'NPN', 'PNP', 'PNP', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN']}}
    # save_scale_to_json(SCALE)