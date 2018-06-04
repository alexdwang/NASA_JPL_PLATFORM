import string
import GUI.Library as Library
import GUI.FILEPATHS as FILEPATHS
import GUI.fit as fit


# generate a Netlist based on the input parameters and save it to ProjectHome/Netlist
class NetListGenerator:
    def generate(self, part, simulation, DR, H2, TID_level, output_option, output_filepath, netlist_filepath): # generate Netlist
        # if simulation == Library.SIMULATION_MODEL or TID_level == Library.TPRE_RAD:
        #     return self.generate_for_compact_model(part, simulation, TID_level, output_option, output_filepath, netlist_filepath)
        # else:
        #     return self.generate_for_current_source_1(part, simulation, TID_level, output_option, output_filepath, netlist_filepath)
        return self.generater(part, simulation, DR, H2, TID_level, output_option, output_filepath, netlist_filepath)

    def generate_for_current_source_1(self, part, simulation, TID_level, output_option, output_filepath, netlist_filepath):
        content = []
        content.extend(['Title: TL431 / Pre Rad / T= 300.15K = 27C',
        '*****************************************',
        '*Input Voltage Source',
        '*********************',
        'V1 1 0 DC 0V',
        '',
        '*Schematic name: TL431 core',
        '***************************',
        '*Subcircuit',
        '*X1 REF K A',
        'X1 2 3 0 TL431_sc',
        '',
        '*Resistance: R<name> <+ node> <- node> [model name] <value>',
        'r21 4 0 6800',
        'r22 5 4 10000',
        'r23 5 1 180',
        '',
        'Vika 5 3 0',
        'Viref 4 2 0',
        '',
        '*Input',
        '.dc V1 0 25 1',
        '',
        '*Output',
        '.print dc format=noindex file=' + FILEPATHS.XDATA_FILE_PATH,
        '+ V(1)',
        '+ V(X1:REF)',
        '+ V(X1:7)',
        '+ V(X1:A)',
        '+ V(X1:16)',
        '+ V(X1:11)',
        '+ V(X1:6)',
        '+ V(X1:1)',
        '+ V(X1:3)',
        '+ V(X1:19)',
        '+ V(X1:18)',
        '+ V(X1:8)',
        '+ V(X1:9)',
        '+ V(X1:12)',
        '+ V(X1:13)',
        '+ {V(X1:REF)-V(X1:7)}',
        '+ {V(X1:16)-V(X1:REF)}',
        '+ {V(X1:12)-V(X1:11)}',
        '+ {V(X1:13)-V(X1:11)}',
        '+ {V(X1:7)-V(X1:6)}',
        '+ {V(X1:1)-V(X1:9)}',
        '+ {V(X1:1)-V(X1:A)}',
        '+ {V(X1:3)-V(X1:A)}',
        '+ {V(X1:8)-V(X1:A)}',
        '+ {V(X1:16)-V(X1:18)}',
        '+ {V(X1:19)-V(X1:A)}',
        '',
        '*Schematic name: TL431_sc',
        '***************************',
        '.subckt TL431_sc REF K A',
        '',
        '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
        'C1 5 3 20p',
        'C2 16 K 20p',
        '',
        '*Resistance: R<name> <+ node> <- node> [model name] <value>',
        'R1 K 13 180',
        'R20 K 12 180',
        'R2 6 5 1100',
        'R5 4 3 2400',
        'R4 4 1 2400',
        'R3 7 4 2500',
        'R8 19 A 4800',
        'R9 19 18 33',
        'R7 8 1 270',
        'R6 9 A 373',
        '',
        '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
        'Q2 K REF 7 QNMOD 2',
        'Q3 16 16 REF QNMOD 3',
        'Q4 11 11 12 QLPMOD 2',
        'Q5 16 11 13 QLPMOD 1',
        'Q6 11 7 6 QNMOD 1',
        'Q7 3 1 9 QNMOD 7.2',
        'Q8 1 1 A QNMOD 0.9',
        'Q9 5 3 A QNMOD 1',
        'Q10 16 8 A QNMOD 1',
        'Q11 K 16 18 QNMOD 2.5',
        'Q12 K 19 A QNMOD 50',
        '',
        '*ends of the TL431_sc subcircuit',
        '.ends',
        '',
        '*Library',
        '* npn prerad off ctp 3b',
        '.model QNMOD NPN (',
        '             ',
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
        '            ',
        '+ IS = 8.70964E-16',
        '+ BF = 786.9		NF = 0.99                           VAF = 36.3423711',
        '+ IKF = 6.30957E-5       NK = 0.52                           ISE = 9.54993E-17',
        '+ NE = 1.27089           BR = 0.697                          NR = 2',
        '+ VAR = 100              IKR = 0.1                           ISC = 1E-17',
        '+ NC = 2                 RB = 758.578                        IRB = 3.6E-5',
        '+ RBM = 100              RE = 4.096                           RC = 1)',
        '',
        '*end of the netlist',
        '.end'])
        try:
            file = open(netlist_filepath, 'wb')
            for line in content:
                text = (line + '\r\n').encode('ascii')
                file.write(text)
            file.close()
            return True
        except:
            return False

    def generate_for_current_source_2(self, part, simulation, TID_level, output_option, output_filepath, netlist_filepath, V0_deltaIb):
        content = []
        content.extend(['Title: TL431 / 20k / T= 300.15K = 27C',
        '*****************************************',
        '',
        '*Input Voltage Source',
        '*********************',
        'V1 1 0 DC 0V',
        '',
        '*Schematic name: TL431 core',
        '***************************',
        '*Subcircuit',
        '*X1 REF K A',
        'X1 2 3 0 TL431_sc',
        '',
        '*Resistance: R<name> <+ node> <- node> [model name] <value>',
        'r21 4 0 6800',
        'r22 5 4 10000',
        'r23 5 1 180',
        '',
        'Vika 5 3 0',
        'Viref 4 2 0',
        '',
        '*Input',
        '.dc V1 '+ V0_deltaIb[0] + ' ' + V0_deltaIb[0] + ' 1',
        '',
        '*Output',
        '.print dc format=noindex file=' + output_filepath,
        '+ V(1)',
        '+ I(Vika)',
        '',
        '*Schematic name: TL431_sc',
        '*************************',
        '.subckt TL431_sc REF K A',
        '*Voltage Controlled Current Source',
        '**********************************',
        'B2 REF 7 I=' + V0_deltaIb[1],
        'B3 16 REF I=' + V0_deltaIb[2],
        'B4 12 11 I='+ V0_deltaIb[3],
        'B5 13 11 I='+ V0_deltaIb[4],
        'B6 7 6 I='+ V0_deltaIb[5],
        'B7 1 9 I='+ V0_deltaIb[6],
        'B8 1 A I='+ V0_deltaIb[7],
        'B9 3 A I='+ V0_deltaIb[8],
        'B10 8 A I='+ V0_deltaIb[9],
        'B11 16 18 I='+ V0_deltaIb[10],
        'B12 19 A I='+ V0_deltaIb[11],
        '',
        '*Capacitance: C<name> <+ node> <- node> [model name] <value> + [IC=<initial value>]',
        'C1 3 5 20p',
        'C2 K 16 20p',
        '',
        '*Resistance: R<name> <+ node> <- node> [model name] <value>',
        'R1 K 13 180',
        'R20 K 12 180',
        'R2 6 5 1100',
        'R5 4 3 2400',
        'R4 4 1 2400',
        'R3 7 4 2500',
        'R8 19 A 4800',
        'R9 19 18 33',
        'R7 8 1 270',
        'R6 9 A 373',
        '',
        '*BJT: Q<name> <collector> <base> <emitter> [substrate] <model name> [area value]',
        'Q2 K REF 7 QNMOD 2',
        'Q3 16 16 REF QNMOD 3',
        'Q6 11 7 6 QNMOD 1',
        'Q7 3 1 9 QNMOD 7.2',
        'Q8 1 1 A QNMOD 0.9',
        'Q9 5 3 A QNMOD 1',
        'Q10 16 8 A QNMOD 1',
        'Q11 K 16 18 QNMOD 2.5',
        'Q12 K 19 A QNMOD 50',
        '',
        'Q4 11 11 12 QLPMOD 2',
        'Q5 16 11 13 QLPMOD 1',
        '',
        '*ends of the TL431_sc subcircuit',
        '.ends',
        '',
        '*Library',
        '* npn prerad off ctp 3b',
        '.model QNMOD NPN (',
        '',
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
        '            ',
        '+ IS = 8.70964E-16',
        '+ BF = 786.9		NF = 0.99                           VAF = 36.3423711',
        '+ IKF = 6.30957E-5       NK = 0.52                           ISE = 9.54993E-17',
        '+ NE = 1.27089           BR = 0.697                          NR = 2',
        '+ VAR = 100              IKR = 0.1                           ISC = 1E-17',
        '+ NC = 2                 RB = 758.578                        IRB = 3.6E-5',
        '+ RBM = 100              RE = 4.096                           RC = 1)',
        '',
        '*end of the netlist',
        '.end'])
        try:
            file = open(netlist_filepath, 'wb')
            for line in content:
                text = (line + '\r\n').encode('ascii')
                file.write(text)
            file.close()
            return True
        except:
            return False

    def generater(self, part, simulation, DR, H2, TID_level, output_option, output_filepath, netlist_filepath):
        content = []
        if TID_level == Library.TPRE_RAD:
            simulation = Library.SIMULATION_MODEL
        try:
            # Section 1: Title
            content.extend(['Title: ' + part + ' / ' + TID_level + ' / ' + 'DR= ' + str(DR) + ' / ' + 'H2= ' + str(H2),
                            ''])
            # Section 2: Input Voltage Source
            content.extend(['*Input Voltage Source',
                            '*********************'])
            temp = Library.INPUT_VOLTAGE_SOURCE.get(part + output_option)
            if temp is None:
                temp = Library.INPUT_VOLTAGE_SOURCE.get(part)
            content.extend(temp)
            content.extend(['*End Input Voltage Source',
                            ''])
            # Section 3: Circuit core
            content.extend(['*Circuit Core',
                            '*************',])
            temp = Library.CIRCUIT_CORE.get(part + output_option)
            if temp is None:
                temp = Library.CIRCUIT_CORE.get(part)
            content.extend(temp)
            content.extend(['*End Circuit Core',
                            ''])

            # # 2 additional sections for current source simulation
            # if simulation == Library.SIMULATION_SOURCE:
            #     # Section Parameters (only if use current source):
            #     content.extend(['*Parameters',
            #                     '***********'])
            #     excel_file_path = Library.EXCEL_FILE_PATH[part]
            #     # a,b,c
            #     if Library.NUM_OF_PARAMETER[part] == 4:
            #         a1, b1, c1 = fit.fit('PNP', Library.TPRE_RAD, excel_file_path)
            #         a2, b2, c2 = fit.fit('PNP', TID_level, excel_file_path)
            #         a3, b3, c3 = fit.fit('NPN', Library.TPRE_RAD, excel_file_path)
            #         a4, b4, c4 = fit.fit('NPN', TID_level, excel_file_path)
            #         paras = ['*PRE_RAD_PNP',
            #                  '.PARAM a1=' + str(a1)[0:8],
            #                  '.PARAM b1=' + str(b1)[0:8],
            #                  '.PARAM c1=' + str(c1)[0:8],
            #                  '',
            #                  '*' + TID_level + 'rad_PNP',
            #                  '.PARAM a2=' + str(a2)[0:8],
            #                  '.PARAM b2=' + str(b2)[0:8],
            #                  '.PARAM c2=' + str(c2)[0:8],
            #                  '',
            #                  '*PRE_RAD_NPN',
            #                  '.PARAM a3=' + str(a3)[0:8],
            #                  '.PARAM b3=' + str(b3)[0:8],
            #                  '.PARAM c3=' + str(c3)[0:8],
            #                  '',
            #                  '*' + TID_level + 'rad_NPN',
            #                  '.PARAM a4=' + str(a4)[0:8],
            #                  '.PARAM b4=' + str(b4)[0:8],
            #                  '.PARAM c4=' + str(c4)[0:8]]
            #         content.extend(paras)
            #     elif Library.NUM_OF_PARAMETER[part] == 2:
            #         fit.fit('LDR', Library.TPRE_RAD, excel_file_path)
            #         fit.fit('LDR', TID_level, excel_file_path)
            #         a1, b1, c1 = fit.fit('LDR', Library.TPRE_RAD, excel_file_path)
            #         a2, b2, c2 = fit.fit('LDR', TID_level, excel_file_path)
            #         paras = ['*PRE_RAD',
            #                  '.PARAM a1=' + str(a1)[0:8],
            #                  '.PARAM b1=' + str(b1)[0:8],
            #                  '.PARAM c1=' + str(c1)[0:8],
            #                  '',
            #                  '*' + TID_level + 'rad',
            #                  '.PARAM a2=' + str(a2)[0:8],
            #                  '.PARAM b2=' + str(b2)[0:8],
            #                  '.PARAM c2=' + str(c2)[0:8],
            #                  ]
            #         content.extend(paras)
            #     # scale
            #     content.append('')
            #     content.extend(Library.SCALE[part])
            #     content.extend(['*End Parameters',
            #                     ''])
            #     # Section Function (only if use current source):
            #     content.extend(['*Function',
            #                     '*********'])
            #     content.extend(Library.FUNCTIONS[part])
            #     content.extend(['*End Function',
            #                     ''])
            # Section 4: Input
            content.extend(['*Input',
                            '******',])
            temp = Library.INPUT.get(part + output_option)
            if temp is None:
                temp = Library.INPUT.get(part)
            content.extend(temp)

            content.extend(['*End Input',
                            ''])
            # Section 5: Output
            content.extend(['*Output',
                            '*******',
                            '.print dc format=noindex file=' + output_filepath])
            content.extend(Library.OUTPUT[part][output_option])
            # content.append(output_option_x)
            # content.append(output_option_y)
            content.extend(['*End Output',
                            ''])
            # Section 6: Subcircuit
            content.extend(['*Subcircuit',
                            '************'])
            content.extend(Library.SUBCIRCUIT[part][simulation])
            content.extend(['*End Subcircuit',
                            ''])
            # Section 7: Library
            content.extend(['*Library',
                            '*******'])
            if simulation == Library.SIMULATION_MODEL:
                content.extend(Library.LIBRARY_TID_LEVEL_MODEL[TID_level])
            else:
                content.extend(Library.LIBRARY_TID_LEVEL_MODEL[Library.TPRE_RAD])
            # Additional library
            if Library.LIBRARY_JFET.get(part) is not None:
                content.extend(Library.LIBRARY_JFET[part]),

            if simulation == Library.SIMULATION_SOURCE:
                # DMOD
                content.extend(['.model DMOD D (IS = 4E-10',
                                '+ RS = .105',
                                '+ N = 1.48',
                                '+ TT = 8E-7',
                                '+ CJO = 1.95E-11',
                                '+ VJ = .4',
                                '+ M = .38',
                                '+ EG = 1.36',
                                '+ XTI = -8',
                                '+ KF = 0',
                                '+ AF = 1',
                                '+ FC = .9',
                                '+ BV = 600',
                                '+ IBV = 1E-4)'])

                a1, b1 = fit.fit('PNP', TID_level, DR, H2)
                a2, b2 = fit.fit('NPN', TID_level, DR, H2)
                # print(TID_level + " a1=" + str(a1) + " a2=" + str(a2))
                # print(TID_level + " b1=" + str(b1) + " b2=" + str(b2))
                # print(TID_level + " N_PNP=" + str(1 / (b1 * 0.02585)) + " N_NPN=" + str(1 / (b2 * 0.02585)))
                content.extend(['.model DMODPNP D (IS = ' + str(a1),
                               '+ N = ' + str(1 / (b1 * 0.02585)) + ' )',
                               '',
                               '.model DMODNPN D (IS = ' + str(a2),
                               '+ N = ' + str(1 / (b2 * 0.02585)) + ')'])
                content.extend(['*End Library',
                                '',
                                '*end of the netlist',
                                '.end'])

            # print content to netlist file
            file = open(netlist_filepath, 'wb')
            for line in content:
                text = (line + '\r\n').encode('ascii')
                file.write(text)
            file.close()
            return True
        except Exception as e:
            # print(e)
            return False
