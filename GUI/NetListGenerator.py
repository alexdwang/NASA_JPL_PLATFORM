import string
import GUI.Library

# generate a Netlist based on the input parameters and save it to ProjectHome/Netlist
class NetListGenerator:
    def generate(self, radiation): # generate Netlist
        content_AD590 = ['Title: AD590 / '+ radiation + ' / T= 300.15K = 27C',
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
                         '.print dc format=noindex file=AD590_' + radiation + '_27C_V1.txt',
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
                         '*Library',]
        content_AD590.extend(GUI.Library.CONST_LIBRARY[radiation])
        content_AD590.extend(['',
                              '*JFET',
                              '.model NJF_TYP NJF (',
                              '+ VTO = -1.0	BETA = 6.2E-4	LAMBDA = 0.003',
                              '+ RD = 0.01      RS = 1e-4',
                              '+ CGS = 3E-12    CGD=1.5E-12     IS=5E-10)',
                              '',
                              '*end of the netlist',
                              '.end'])
        file = open("./Netlist/test.cir", 'wb')
        for line in content_AD590:
            text = (line + '\r\n').encode('ascii')
            file.write(text)
        file.close()
        pass