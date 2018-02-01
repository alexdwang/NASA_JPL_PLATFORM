import string
import GUI.Library

# generate a Netlist based on the input parameters and save it to ProjectHome/Netlist
class NetListGenerator:
    def generate(self, part, TID_level, output_filepath, netlist_filepath): # generate Netlist
        if part == GUI.Library.PARTS[0]:
            content = self.content_LT1175(TID_level, output_filepath)
        elif part == GUI.Library.PARTS[1]:
            content = self.content_AD590(TID_level, output_filepath)
        file = open(netlist_filepath, 'wb')
        for line in content:
            text = (line + '\r\n').encode('ascii')
            file.write(text)
        file.close()
        return

    def content_AD590(self, TID_level, output_filepath):
        content_AD590 = ['Title: AD590 / ' + TID_level + ' / T= 300.15K = 27C',
                         '*',
                         '',
                         '*Voltage Source',
                         'VIN 1 0 DC 0V',
                         '',
                         '*Umbrella circuit',
                         'X1 1 2 AD590_sc',
                         'ROUT 2 0 1m',
                         '',
                         '*Input',
                         '.dc VIN 0 30 0.01',
                         '',
                         '*Output',
                         # '.print dc format=noindex file=AD590_' + TID_level + '_27C_V1.txt',
                         '.print dc format=noindex file=' + output_filepath,
                         '+ V(1)',
                         '+ I(ROUT)',
                         '',
                         '*Subcircuit',
                         '.subckt AD590_sc IN OUT',
                         '',
                         '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
                         'c1 1 8 26p',
                         '',
                         '*Resistance: R<name> <+ node> <- node> [model name] <value>',
                         'r1 IN 4 260',
                         'r2 IN 3 1040',
                         'r3 5 16 5000',
                         'r4 11 5 11000',
                         'r5 12 OUT 146',
                         'r6 15 OUT 820',
                         '',
                         '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
                         'Q11 1 5 12 QNMOD 35 temp=27',
                         'Q10 5 5 12 QNMOD 35 temp=27',
                         'Q9 6 5 15 QNMOD 280 temp=27',
                         'Q6 7 7 IN QLPMOD 10 temp=27',
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
                         '.ends',
                         '',
                         '*Library', ]
        content_AD590.extend(GUI.Library.TID_LEVEL_MODEL[TID_level])
        content_AD590.extend(['',
                              '*JFET',
                              '.model NJF_TYP NJF (',
                              '+ VTO = -1.0	BETA = 6.2E-4	LAMBDA = 0.003',
                              '+ RD = 0.01      RS = 1e-4',
                              '+ CGS = 3E-12    CGD=1.5E-12     IS=5E-10)',
                              '',
                              '*end of the netlist',
                              '.end'])
        return content_AD590

    def content_LT1175(self, TID_level, output_filepath):
        content_LT1175=['Title: LT1175 / Line Regulation / ' + TID_level + ' / T= 300.15K = 27C',
                        '',
                        '*Input Voltage Source',
                        'V2 4 0 DC 0V',
                        '',
                        '*Schematic name: LT1175 core',
                        '****************************',
                        '*Subcircuit',
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
                        'Q2 0 7 2 QNMOD 10',
                        '',
                        '*Input',
                        '.dc V2 0 -20 -0.1',
                        '',
                        '*Output',
                        '.print dc format=noindex file=' + output_filepath,
                        '+ V(4)',
                        '+ V(1)',
                        '',
                        '',
                        '*Schematic name: BG_sc',
                        '**********************',
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
                        '',
                        '*Schematic name: OPAMP_sc',
                        '*************************',
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
                        '.ends OPAMP_sc',
                        '',
                        '*Library',
                        '********',
                        '* npn prerad off ctp 3b',
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
                        '+ RBM = 100              RE = 4.096                           RC = 1)',
                        '',
                        '*end of the netlist',
                        '.end',
                        ]
        return content_LT1175