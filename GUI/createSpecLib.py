import json

import GUI.FILEPATHS as FILEPATHS
import GUI.saveJson as saveJson


def save_specification_to_json(SPECIFICATION):
    output_object = SPECIFICATION
    with open("../" + FILEPATHS.SPECIFICATION_FILE_PATH, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return

# SPECIFICATION = {PART_NAME: OUTPUT: [MIN, MAX]}
SPECIFICATION = {saveJson.PART_AD590: {'Output Current': []},

                 saveJson.PART_LT1175: {'Line Regulation': []},

                 saveJson.PART_TL431: {'Vref': [2.44, 2.55],
                                       'Iref': [],
                                       'Ika': [],
                                       'Vka': []}}

save_specification_to_json(SPECIFICATION)