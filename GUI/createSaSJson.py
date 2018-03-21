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

# SPECIFICATION = {PART_NAME: OUTPUT: [MIN, MAX]}
SPECIFICATION = {createNaLJson.PART_AD590: {'Output Current': []},

                 createNaLJson.PART_LT1175: {'Line Regulation': []},

                 createNaLJson.PART_TL431: {'Vref': [2.44, 2.55],
                                       'Iref': [],
                                       'Ika': [],
                                       'Vka': []}}

save_specification_to_json(SPECIFICATION)

SCALE = {createNaLJson.PART_TL431: {'scale': [2, 3, 2, 1, 1, 7.2, 0.9, 1, 1, 2.5, 50],
                                    'type': ['NPN', 'NPN', 'PNP', 'PNP', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN', 'NPN']}}
save_scale_to_json(SCALE)