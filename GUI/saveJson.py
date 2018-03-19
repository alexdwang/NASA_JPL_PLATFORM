import json
import GUI.FILEPATHS as FILEPATHS


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
    with open("../" + FILEPATHS.NAME_FILE_PATH, 'w') as f:
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

    with open("../" + FILEPATHS.LIBRARY_FILE_PATH, 'w') as f:
        json.dump(output_object, f)
    f.close()
    return

# names
TITLE = 'NASA JPL Platform'
PART_LT1175 = 'LT1175'
PART_AD590 = 'AD590'
PARTS = [PART_LT1175, PART_AD590]
SIMULATION_MODEL = 'compact model'
SIMULATION_SOURCE = 'external current source'
SIMULATION = [SIMULATION_MODEL, SIMULATION_SOURCE]
TPRE_RAD = 'pre_rad'
T2_5KRAD = '2.5k'
T5KRAD = '5k'
T10KRAD = '10k'
T20KRAD = '20k'
T30KRAD = '30k'
T50KRAD = '50k'
T100KRAD = '100k'
T200KRAD = '200k'
T300KRAD = '300k'
TID_LEVEL = [TPRE_RAD,        # 0
             T2_5KRAD,        # 1
             T5KRAD,          # 2
             T10KRAD,         # 3
             T20KRAD,         # 4
             T30KRAD,         # 5
             T50KRAD,         # 6
             T100KRAD,        # 7
             T200KRAD,        # 8
             T300KRAD         # 9
             ]
TID_LIST = {SIMULATION_MODEL: [
                                TPRE_RAD,
                                T2_5KRAD,
                                T5KRAD,
                                T10KRAD,
                                T20KRAD,
                                T30KRAD,
                                T50KRAD,
                                T100KRAD,
                                T200KRAD,
                                T300KRAD],
            SIMULATION_SOURCE: [
                                T2_5KRAD,
                                T5KRAD,
                                T10KRAD,
                                T20KRAD,
                                T30KRAD,
                                T50KRAD,
                                T100KRAD,
                                T200KRAD,
                                T300KRAD],
            }

# Excel file path
EXCEL_FILE_PATH = {PART_AD590: 'FitCurve/NPN_PNP_Data_Yidi.xlsx',
                   PART_LT1175: 'FitCurve/PNP_FITTING.xlsx'}

# Excel sheet name & column name
COL_NAME = {'VE':       'Ve_PRE_RAD',
            TPRE_RAD:   'Ib_PRE_RAD',
            T2_5KRAD:   'Ib_2.5krad',
            T5KRAD:     'Ib_5krad',
            T10KRAD:    'Ib_10krad',
            T20KRAD:    'Ib_20krad',
            T30KRAD:    'Ib_30krad',
            T50KRAD:    'Ib_50krad',
            T100KRAD:   'Ib_100krad',
            T200KRAD:   'Ib_200krad',
            T300KRAD:   'Ib_300krad'}

SHEET_NAME = {'NPN': 'NPN_Compact_Xyce',
              'PNP': 'PNP_Compact_Xyce',
              'LDR': 'LDR_1_FIT_0.4V',
              'HDR': 'HDR'}
NUM_OF_PARAMETER = {PART_AD590: 4,
                    PART_LT1175: 2}
save_name_to_json(TITLE, PARTS, SIMULATION, TID_LEVEL, TID_LIST, EXCEL_FILE_PATH, COL_NAME, SHEET_NAME, NUM_OF_PARAMETER)

# circuit code library
                        # LT1175:
INPUT_VOLTAGE_SOURCE = {PART_LT1175: ['V2 4 0 DC 0V'],

                        # AD590:
                        PART_AD590: ['VIN 2 0 DC 0V',
                                     'VOUT 20 0 0']
                        }

CIRCUIT_CORE = {PART_LT1175: ['*Subcircuit',
                           '*X1 VCC VEE VREF',
                           'X1 0 4 5 BG_sc',
                           '',
                           '*X4 V+ V- VCC VEE VO',
                           'X4 6 5 0 4 7 OPAMP_sc',
                           '',
                           '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                           'r1 0 6 350k',
                           'r2 6 1 100k',
                           'rLIM 3 4 0.001',
                           '',
                           '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                           'Q1 1 2 3 QNMOD 1000',
                           'Q2 0 7 2 QNMOD 10'],
                PART_AD590: [
                             'XZ 2 20 AD590',
                             'R0 20 0 1m'
                ]
                }

SCALE = {PART_LT1175: ['*SCALE',
                       '.PARAM scale1=1',
                       '.PARAM scale2=1',
                       '.PARAM scale3=1',
                       '.PARAM scale4=0.1',
                       '',
                       '.PARAM scale6=20',
                       '.PARAM scale7=20',
                       '.PARAM scale8=1',
                       '.PARAM scale9=10',
                       '.PARAM scale10=10'],
         PART_AD590: ['*SCALE',
                       '.PARAM scale1=10',
                       '.PARAM scale2=10',
                       '.PARAM scale3=10',
                       '.PARAM scale4=10',
                       '.PARAM scale5=10',
                       '.PARAM scale6=10',
                       '.PARAM scale7=10',
                       '.PARAM scale8=10',
                       '.PARAM scale9=280',
                       '.PARAM scale10=35',
                       '.PARAM scale11=35']}

FUNCTIONS = {PART_LT1175: ['*DeltaIb = 1*(exp(a2+(b2*Veb)+(c2*(Veb*Veb))) - exp(a1+(b1*Veb)+(c1*(Veb*Veb))))',
                          '*.func deltaIb(x) {scale*(exp(a2+(b2*x)+(c2*(pow(x,2)))) - exp(a1+(b1*x)+(c1*(pow(x,2)))))}',
                          '.func deltaIb1(x) {scale1*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '.func deltaIb2(x) {scale2*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '.func deltaIb3(x) {scale3*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '.func deltaIb4(x) {scale4*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '',
                          '.func deltaIb6(x) {scale6*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '.func deltaIb7(x) {scale7*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '.func deltaIb8(x) {scale8*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '.func deltaIb9(x) {scale9*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}',
                          '.func deltaIb10(x) {scale10*(exp(a2+(b2*x)+(c2*(x*x))) - exp(a1+(b1*x)+(c1*(x*x))))}'],
             PART_AD590: ['*DeltaIb = 1*(exp(a2+(b2*Veb)+(c2*(Veb*Veb))) - exp(a1+(b1*Veb)+(c1*(Veb*Veb))))',
                         '*.func deltaIb(x) {scale*(exp(a2+(b2*x)+(c2*(pow(x,2)))) - exp(a1+(b1*x)+(c1*(pow(x,2)))))}',
                         '*PNP',
                         '.func deltaIb1(x) {scale1*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                         '.func deltaIb2(x) {scale2*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                         '.func deltaIb3(x) {scale3*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                         '.func deltaIb4(x) {scale4*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                         '.func deltaIb5(x) {scale5*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                         '.func deltaIb6(x) {scale6*((exp(a2+(b2*x)+(c2*(x*x)))) - (exp(a1+(b1*x)+(c1*(x*x)))))}',
                         '',
                         '*NPN',
                         '.func deltaIb7(x) {scale7*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                         '.func deltaIb8(x) {scale8*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                         '.func deltaIb9(x) {scale9*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                         '.func deltaIb10(x) {scale10*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}',
                         '.func deltaIb11(x) {scale11*((exp(a4+(b4*x)+(c4*(x*x)))) - (exp(a3+(b3*x)+(c3*(x*x)))))}']}

INPUT = {PART_LT1175: ['.dc V2 0 -20 -0.1'],
         PART_AD590: ['.dc VIN 0 30 0.01']
         }
OUTPUT_OPTION = {PART_LT1175: ['+ V(4)',
                               '+ V(1)'],
                 PART_AD590: ['+ V(2)',
                              '+ I(VOUT)']}
OUTPUT = {PART_LT1175: {'Line Regulation': ['+ V(4)',
                                               '+ V(1)']},
          PART_AD590: {'Default': ['+ V(2)',
                                              '+ I(VOUT)']}}
SUBCIRCUIT = {PART_LT1175: {SIMULATION_MODEL: [
                                '.subckt BG_sc VCC VEE VREF',
                                '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                                'r1 VCC 1 10k',
                                'r2 1 8 2.93e6',
                                'r3 8 9 109k',
                                'r4 4 VEE 600',
                                'r5 6 VEE 600',
                                '',
                                '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                                'Q1 2 2 VCC QLPMOD 1',
                                'Q2 3 2 1 QLPMOD 1',
                                'Q3 12 5 9 QLPMOD 1',
                                'Q4 11 5 8 QLPMOD 0.1',
                                'Q5 12 12 7 QNMOD 1',
                                'Q6 11 12 7 QNMOD 1',
                                'Q7 VCC 5 7 QNMOD 1',
                                'Q8 3 3 4 QNMOD 1',
                                'Q9 7 3 6 QNMOD 1',
                                '',
                                '*Voltage Controlled Voltage Source: E<name> <+ node> <-node> <+ controlling node> <- controlling node> <gain>',
                                'E1 VCC VREF VCC 5 1',
                                '',
                                '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                                'I1 2 0 DC 3.23uA',
                                '',
                                '*end of the BG_sc subcircuit',
                                '.ends BG_sc',
                                '',
                                '.subckt OPAMP_sc V10 V11 VCC VEE VO',
                                '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                                'r1 7 VEE 4.7k',
                                'r2 3 VEE 4.7k',
                                'r3 VO VEE 60k',
                                'r4 11 VEE 60k',
                                '',
                                '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                                'C1 1 9 0.0056p',
                                '',
                                '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                                'Q1 1 11 VEE QNMOD 10',
                                'Q2 VCC 1 VO QNMOD 1',
                                'Q3 VCC 9 11 QNMOD 1',
                                'Q4 9 4 7 QNMOD 1',
                                'Q5 4 4 3 QNMOD 1',
                                'Q6 9 V10 5 QLPMOD 20',
                                'Q7 4 V11 5 QLPMOD 20',
                                'Q8 6 6 VCC QLPMOD 1',
                                'Q9 5 6 VCC QLPMOD 10',
                                'Q10 1 6 VCC QLPMOD 10',
                                '',
                                '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                                'I1 6 0 DC 1.4u',
                                '',
                                '*end of the OPAMP_sc subcircuit',
                                '.ends OPAMP_sc'],
                            SIMULATION_SOURCE: [
                                '.subckt BG_sc VCC VEE VREF',
                                  '*Voltage Controlled Current Source BG',
                                  'B1 VCC 2 I={deltaIb1(V(VCC)-V(2))}',
                                  'B2 1 2 I={deltaIb2(V(1)-V(2))}',
                                  'B3 9 5 I={deltaIb3(V(9)-V(5))}',
                                  'B4 8 5 I={deltaIb4(V(8)-V(5))}',
                                  '',
                                  '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                                  'r1 VCC 1 10k',
                                  'r2 1 8 2.93e6',
                                  'r3 8 9 109k',
                                  'r4 4 VEE 600',
                                  'r5 6 VEE 600',
                                  '',
                                  '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                                  'Q1 2 2 VCC QLPMOD 1',
                                  'Q2 3 2 1 QLPMOD 1',
                                  'Q3 12 5 9 QLPMOD 1',
                                  'Q4 11 5 8 QLPMOD 0.1',
                                  'Q5 12 12 7 QNMOD 1',
                                  'Q6 11 12 7 QNMOD 1',
                                  'Q7 VCC 5 7 QNMOD 1',
                                  'Q8 3 3 4 QNMOD 1',
                                  'Q9 7 3 6 QNMOD 1',
                                  '',
                                  '*Voltage Controlled Voltage Source: E<name> <+ node> <-node> <+ controlling node> <- controlling node> <gain>',
                                  'E1 VCC VREF VCC 5 1',
                                  '',
                                  '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                                  'I1 2 0 DC 3.23uA',
                                  '',
                                  '*end of the BG_sc subcircuit',
                                  '.ends BG_sc',
                                  '',
                                  '',
                                  '.subckt OPAMP_sc V10 V11 VCC VEE VO',
                                  '',
                                  '*Voltage Controlled Current Source OPAMP',
                                  'B6 5 V10 I={deltaIb6(V(5)-V(V10))}',
                                  'B7 5 V11 I={deltaIb7(V(5)-V(V11))}',
                                  'B8 6 VCC I={deltaIb8(V(6)-V(VCC))}',
                                  'B9 6 VCC I={deltaIb9(V(6)-V(VCC))}',
                                  'B10 6 VCC I={deltaIb10(V(6)-V(VCC))}',
                                  '',
                                  '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                                  'r1 7 VEE 4.7k',
                                  'r2 3 VEE 4.7k',
                                  'r3 VO VEE 60k',
                                  'r4 11 VEE 60k',
                                  '',
                                  '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                                  'C1 1 9 0.0056p',
                                  '',
                                  '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                                  'Q1 1 11 VEE QNMOD 10',
                                  'Q2 VCC 1 VO QNMOD 1',
                                  'Q3 VCC 9 11 QNMOD 1',
                                  'Q4 9 4 7 QNMOD 1',
                                  'Q5 4 4 3 QNMOD 1',
                                  'Q6 9 V10 5 QLPMOD 20',
                                  'Q7 4 V11 5 QLPMOD 20',
                                  'Q8 6 6 VCC QLPMOD 1',
                                  'Q9 5 6 VCC QLPMOD 10',
                                  'Q10 1 6 VCC QLPMOD 10',
                                  '',
                                  '*Independent Current Source: I<name> <+ node> <-node> [[DC] <value>]',
                                  'I1 6 0 DC 1.4u',
                                  '',
                                  '*end of the OPAMP_sc subcircuit',
                                  '.ends OPAMP_sc']},
              PART_AD590: {SIMULATION_MODEL: ['.subckt AD590 2 20',
                                           '',
                                           '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                                           'c1 1 8 26p',
                                           '',
                                           '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                                           'r1 2 4 260',
                                           'r2 2 3 1040',
                                           'r3 5 16 5000',
                                           'r4 11 5 11000',
                                           'r5 12 20 146',
                                           'r6 15 20 820',
                                           '',
                                           '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                                           'Q11 1 5 12 QNMOD 35 temp=27',
                                           'Q10 5 5 12 QNMOD 35 temp=27',
                                           'Q9 6 5 15 QNMOD 280 temp=27',
                                           'Q6 7 7 2 QLPMOD 10 temp=27',
                                           'Q4 1 8 4 QLPMOD 10 temp=27',
                                           'Q3 1 8 4 QLPMOD 10 temp=27',
                                           'Q5 8 8 3 QLPMOD 10 temp=27',
                                           'Q2 6 8 4 QLPMOD 10 temp=27',
                                           'Q1 6 8 4 QLPMOD 10 temp=27',
                                           'Q7 7 6 11 QNMOD 10 temp=27',
                                           'Q8 8 1 11 QNMOD 10 temp=27',
                                           '',
                                           '*JFET: J<name> <drain> <gate> <source> <model name> [area value]',
                                           'J1 8 16 11 NJF_TYP',
                                           '',
                                           '*end of the subcircuit',
                                           '.ends'],
                           SIMULATION_SOURCE: ['.subckt AD590 2 20',
                                           '',
                                           '*Voltage Controlled Current Source',
                                           '*PNP',
                                           'B1 4 8 I={deltaIb1(V(4)-V(8))}',
                                           'B2 4 8 I={deltaIb2(V(4)-V(8))}',
                                           'B3 4 8 I={deltaIb3(V(4)-V(8))}',
                                           'B4 4 8 I={deltaIb4(V(4)-V(8))}',
                                           'B5 3 8 I={deltaIb5(V(3)-V(8))}',
                                           'B6 2 7 I={deltaIb6(V(2)-V(7))}',
                                           '*NPN',
                                           'B7 6 11 I={deltaIb7(V(6,11))}',
                                           'B8 1 11 I={deltaIb8(V(1,11))}',
                                           'B9 5 15 I={deltaIb9(V(5,15))}',
                                           'B10 5 12 I={deltaIb10(V(5,12))}',
                                           'B11 5 12 I={deltaIb11(V(5,12))}',
                                           '',
                                           '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                                           'c1 1 8 26p',
                                           '',
                                           '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                                           'r1 2 4 260',
                                           'r2 2 3 1040',
                                           'r3 5 16 5000',
                                           'r4 11 5 11000',
                                           'r5 12 20 146',
                                           'r6 15 20 820',
                                           '',
                                           '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                                           'Q11 1 5 12 QNMOD 35 temp=27',
                                           'Q10 5 5 12 QNMOD 35 temp=27',
                                           'Q9 6 5 15 QNMOD 280 temp=27',
                                           'Q6 7 7 2 QLPMOD 10 temp=27',
                                           'Q4 1 8 4 QLPMOD 10 temp=27',
                                           'Q3 1 8 4 QLPMOD 10 temp=27',
                                           'Q5 8 8 3 QLPMOD 10 temp=27',
                                           'Q2 6 8 4 QLPMOD 10 temp=27',
                                           'Q1 6 8 4 QLPMOD 10 temp=27',
                                           'Q7 7 6 11 QNMOD 10 temp=27',
                                           'Q8 8 1 11 QNMOD 10 temp=27',
                                           '',
                                           '*JFET: J<name> <drain> <gate> <source> <model name> [area value]',
                                           'J1 8 16 11 NJF_TYP',
                                           '',
                                           '*end of the subcircuit',
                                           '.ends']}
              }

LIBRARY_TID_LEVEL_MODEL = {TPRE_RAD: ['* npn prerad off ctp 3b',
                                      '.model QNMOD NPN (',
                                      '+ IS = 1.68208E-16',
                                      '+ BF = 84.058    NF = 0.986787 VAF = 351.9861415',
                                      '+ IKF = 9.86E-3  NK = 0.47574  ISE = 7.1029E-15',
                                      '+ NE = 2.06453   BR = 0.697    NR = 2',
                                      '+ VAR = 100      IKR = 0.1     ISC = 1E-17',
                                      '+ NC = 2         RB = 140.86   IRB = 1E-3',
                                      '+ RBM = 50       RE = 2        RC = 250.75)',
                                      '',
                                      '*lpnp prerad off ctp 3b',
                                      '.model QLPMOD PNP (',
                                      '+ IS = 8.70964E-16',
                                      '+ BF = 786.9		NF = 0.99                           VAF = 36.3423711',
                                      '+ IKF = 6.30957E-5       NK = 0.52                           ISE = 9.54993E-17',
                                      '+ NE = 1.27089           BR = 0.697                          NR = 2',
                                      '+ VAR = 100              IKR = 0.1                           ISC = 1E-17',
                                      '+ NC = 2                 RB = 758.578                        IRB = 3.6E-5',
                                      '+ RBM = 100              RE = 4.096                           RC = 1)'
                                      ],

                           T20KRAD: ['* npn 2e4 off ctp 3b',
                                   '.model QNMOD NPN  (                      ',
                                   '+ IS     = 1.68208E-16',
                                   '+ BF     = 45.95           NF     = 0.986787        VAF    = 345.2016293',
                                   '+ IKF    = 0.0229087       NK     = 0.47574         ISE    = 1.122018E-14',
                                   '+ NE     = 1.65            BR     = 0.697           NR     = 2',
                                   '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                   '+ NC     = 2               RB     = 140.86          IRB    = 1E-3',
                                   '+ RBM    = 50              RE     = 2               RC     = 250.75)',
                                   '',
                                   '* lpnp 2e4 off ctp 3b',
                                   '.model QLPMOD PNP (',
                                   '+ IS     = 8.70964E-16',
                                   '+ BF     = 264.9           NF     = 0.99            VAF    = 35.8970174',
                                   '+ IKF    = 9.549926E-5     NK     = 0.52            ISE    = 5.495409E-14',
                                   '+ NE     = 1.42            BR     = 0.697           NR     = 2',
                                   '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                   '+ NC     = 2               RB     = 1E3             IRB    = 3.6E-5',
                                   '+ RBM    = 100             RE     = 4.096           RC     = 1)'
                                     ],

                           T50KRAD: ['* npn 5e4 off ctp 3b',
                                     '.model QNMOD NPN  (',
                                     '+ IS     = 1.684E-16',
                                     '+ BF     = 38.7            NF     = 0.986787        VAF    = 342.7968454',
                                     '+ IKF    = 0.0251189       NK     = 0.47574         ISE    = 1.41254E-13',
                                     '+ NE     = 1.82            BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 170.83          IRB    = 1E-3',
                                     '+ RBM    = 50              RE     = 2               RC     = 366.4)',
                                     '',
                                     '* lpnp 5e4 off ctp 3b',
                                     '.model QLPMOD PNP (',
                                     '+ IS     = 1E-15',
                                     '+ BF     = 47.4            NF     = 0.99            VAF    = 34.9777903',
                                     '+ IKF    = 1.09648E-4      NK     = 0.37            ISE    = 1.65959E-13',
                                     '+ NE     = 1.44            BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 1.90546E3       IRB    = 3.16228E-5',
                                     '+ RBM    = 57.544          RE     = 7.093           RC     = 1)'
                                     ],

                           T100KRAD: ['* npn 1e5 off ctp 3b',
                                     '.model QNMOD NPN  (',
                                     '+ IS     = 1.68208E-16',
                                     '+ BF     = 45.95           NF     = 0.986787        VAF    = 342.3319825',
                                     '+ IKF    = 0.0229087       NK     = 0.47574         ISE    = 2.238721E-13',
                                     '+ NE     = 1.701           BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 140.86          IRB    = 1E-3',
                                     '+ RBM    = 50              RE     = 2               RC     = 250.75)'
                                     '',
                                     '* lpnp 1e5 off ctp 3b',
                                     '.model QLPMOD PNP (',
                                     '+ IS     = 1E-15',
                                     '+ BF     = 47.4            NF     = 0.99            VAF    = 33.7331598',
                                     '+ IKF    = 1.09648E-4      NK     = 0.37            ISE    = 2.884032E-13',
                                     '+ NE     = 1.44            BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 1.737801E3      IRB    = 3.16228E-5',
                                     '+ RBM    = 57.544          RE     = 7.093           RC     = 1               )',
                                      ],

                           T200KRAD: ['* npn 2e5 off ctp 3b',
                                     '.model QNMOD NPN  (',
                                     '+ IS     = 1.684E-16',
                                     '+ BF     = 38.7            NF     = 0.986787        VAF    = 313.65875',
                                     '+ IKF    = 0.0251189       NK     = 0.47574         ISE    = 1.28825E-12',
                                     '+ NE     = 1.854           BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 170.83          IRB    = 1E-3',
                                     '+ RBM    = 50              RE     = 2               RC     = 366.4)',
                                     '',
                                     '* lpnp 2e5 off ctp 3b',
                                     '.model QLPMOD PNP (',
                                     '+ IS     = 1E-15',
                                     '+ BF     = 38.7            NF     = 0.99            VAF    = 32.8110824',
                                     '+ IKF    = 1.09648E-4      NK     = 0.37            ISE    = 3.31131E-13',
                                     '+ NE     = 1.44            BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 1.58489E3       IRB    = 3.16228E-5',
                                     '+ RBM    = 57.544          RE     = 7.093           RC     = 1)'
                                      ],

                           T300KRAD: ['* npn 3e5 off ctp 3b',
                                     '.model QNMOD NPN (',
                                     '+ IS     = 1.684E-16',
                                     '+ BF     = 38.7            NF     = 0.986787        VAF    = 329.7773204',
                                     '+ IKF    = 0.0251189       NK     = 0.47574         ISE    = 2.089296E-12',
                                     '+ NE     = 1.871           BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 170.83          IRB    = 1E-3',
                                     '+ RBM    = 50              RE     = 2               RC     = 366.4     )',
                                     '',
                                     '* lpnp 3e5 off ctp 3b',
                                     '.model QLPMOD PNP (',
                                     '+ IS     = 1E-15',
                                     '+ BF     = 33              NF     = 0.99            VAF    = 33.1203665',
                                     '+ IKF    = 1.09648E-4      NK     = 0.37            ISE    = 3.801894E-13',
                                     '+ NE     = 1.44            BR     = 0.697           NR     = 2',
                                     '+ VAR    = 100             IKR    = 0.1             ISC    = 1E-17',
                                     '+ NC     = 2               RB     = 1.58489E3       IRB    = 3.16228E-5',
                                     '+ RBM    = 57.544          RE     = 7.093           RC     = 1               )'
                                      ]
                           }
LIBRARY_JFET = {PART_LT1175: [],
        PART_AD590: ['',
                            '*JFET',
                            '.model NJF_TYP NJF (',
                            '+ VTO = -1.0	BETA = 6.2E-4	LAMBDA = 0.003',
                            '+ RD = 0.01      RS = 1e-4',
                            '+ CGS = 3E-12    CGD=1.5E-12     IS=5E-10)',
                            '']}
save_library_to_json(INPUT_VOLTAGE_SOURCE, CIRCUIT_CORE, SCALE, FUNCTIONS, INPUT, OUTPUT_OPTION, OUTPUT,
                         SUBCIRCUIT, LIBRARY_TID_LEVEL_MODEL, LIBRARY_JFET)

# with open(CONSTANT.LIBRARY_FILE_PATH,'r') as f:
#     jsonObject = f.readline()
# f.close()
# json_dict = json.loads(jsonObject)

# LT1175_OUTPUT_OPTION.append('BBB')
# LT1175_OUTPUT_OPTION = list(set(LT1175_OUTPUT_OPTION))
# OUTPUT[PART_LT1175]['BBB'] = ['+ V(4)',
#                                       '+ V(5)',
#                                       '+ V(1)']
#
# output_object = {'LT1175_OUTPUT_OPTION': LT1175_OUTPUT_OPTION,
#                  'AD590_OUTPUT_OPTION': AD590_OUTPUT_OPTION,
#                  'OUTPUT': OUTPUT}
# with open(LIBRARY_FILE_PATH, 'w') as f:
#     json.dump(output_object, f)
# f.close()
