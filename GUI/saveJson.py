import json

PART_LT1175 = 'LT1175'
PART_AD590 = 'AD590'

# LT1175_OUTPUT_OPTION = ['Line_Regulation']
#
# AD590_OUTPUT_OPTION = ['Default']
#
# OUTPUT = {PART_LT1175: {LT1175_OUTPUT_OPTION[0]: ['+ V(4)',
#                                                '+ V(1)']},
#           PART_AD590: {AD590_OUTPUT_OPTION[0]: ['+ V(2)',
#                                               '+ I(VOUT)']}}
#
# output_object = {'LT1175_OUTPUT_OPTION': LT1175_OUTPUT_OPTION,
#                  'AD590_OUTPUT_OPTION': AD590_OUTPUT_OPTION,
#                  'OUTPUT': OUTPUT}
# with open("output.json",'w') as f:
#     json.dump(output_object, f)
# f.close()

with open("output.json",'r') as f:
    jsonObject = f.readline()
f.close()
json_dict = json.loads(jsonObject)

LT1175_OUTPUT_OPTION = json_dict['LT1175_OUTPUT_OPTION']
AD590_OUTPUT_OPTION = json_dict['AD590_OUTPUT_OPTION']
OUTPUT = json_dict['OUTPUT']

print(OUTPUT)
print(OUTPUT[PART_LT1175])
print(OUTPUT[PART_LT1175][LT1175_OUTPUT_OPTION[0]])

LT1175_OUTPUT_OPTION.append('BBB')
LT1175_OUTPUT_OPTION = list(set(LT1175_OUTPUT_OPTION))
OUTPUT[PART_LT1175]['BBB'] = ['+ V(4)',
                                      '+ V(5)',
                                      '+ V(1)']

output_object = {'LT1175_OUTPUT_OPTION': LT1175_OUTPUT_OPTION,
                 'AD590_OUTPUT_OPTION': AD590_OUTPUT_OPTION,
                 'OUTPUT': OUTPUT}
with open("output.json", 'w') as f:
    json.dump(output_object, f)
f.close()
