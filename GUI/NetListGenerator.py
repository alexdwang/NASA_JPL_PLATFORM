import string
import GUI.Library as Library
import GUI.fit as fit

# generate a Netlist based on the input parameters and save it to ProjectHome/Netlist
class NetListGenerator:
    def generate(self, part, simulation, TID_level, output_option, output_filepath, netlist_filepath): # generate Netlist
        content = []
        # Section 1: Title
        content.extend(['Title: ' + part + ' / ' + TID_level + ' / ' + 'T= 300.15K = 27C',
                        ''])
        # Section 2: Input Voltage Source
        content.extend(['*Input Voltage Source',
                        '***************'])
        content.extend(Library.INPUT_VOLTAGE_SOURCE[part])
        content.append('')
        # Section 3: Circuit core
        content.extend(['*Circuit Core',
                        '*************',])
        content.extend(Library.CIRCUIT_CORE[part])
        content.append('')

        # 2 additional sections for current source simulation
        if simulation == Library.SIMULATION_SOURCE:
            # Section Parameters (only if use current source):
            content.extend(['*Parameters',
                            '***********'])
            excel_file_path = Library.EXCEL_FILE_PATH[part]
            # a,b,c
            if part == Library.PART_AD590:
                a1, b1, c1 = fit.fit('PNP', Library.TPRE_RAD, excel_file_path)
                a2, b2, c2 = fit.fit('PNP', TID_level, excel_file_path)
                a3, b3, c3 = fit.fit('NPN', Library.TPRE_RAD, excel_file_path)
                a4, b4, c4 = fit.fit('NPN', TID_level, excel_file_path)
                paras = ['*PRE_RAD_PNP',
                         '.PARAM a1=' + str(a1)[0:8],
                         '.PARAM b1=' + str(b1)[0:8],
                         '.PARAM c1=' + str(c1)[0:8],
                         '',
                         '*' + TID_level + 'rad_PNP',
                         '.PARAM a2=' + str(a2)[0:8],
                         '.PARAM b2=' + str(b2)[0:8],
                         '.PARAM c2=' + str(c2)[0:8],
                         '',
                         '*PRE_RAD_NPN',
                         '.PARAM a3=' + str(a3)[0:8],
                         '.PARAM b3=' + str(b3)[0:8],
                         '.PARAM c3=' + str(c3)[0:8],
                         '',
                         '*' + TID_level + 'rad_NPN',
                         '.PARAM a4=' + str(a4)[0:8],
                         '.PARAM b4=' + str(b4)[0:8],
                         '.PARAM c4=' + str(c4)[0:8]]
                content.extend(paras)
            elif part == Library.PART_LT1175:
                a1, b1, c1 = fit.fit('LDR', Library.TPRE_RAD, excel_file_path)
                a2, b2, c2 = fit.fit('LDR', TID_level, excel_file_path)
                paras = ['*PRE_RAD',
                         '.PARAM a1=' + str(a1)[0:8],
                         '.PARAM b1=' + str(b1)[0:8],
                         '.PARAM c1=' + str(c1)[0:8],
                         '',
                         '*' + TID_level + 'rad',
                         '.PARAM a2=' + str(a2)[0:8],
                         '.PARAM b2=' + str(b2)[0:8],
                         '.PARAM c2=' + str(c2)[0:8],
                         ]
                content.extend(paras)
            # scale
            content.append('')
            content.extend(Library.SCALE[part])
            content.append('')
            # Section Function (only if use current source):
            content.extend(['*Function'
                            '*********'])
            content.extend(Library.FUNCTIONS[part])
            content.append('')
        # Section 4: Input
        content.extend(['*Input',
                        '******',])
        content.extend(Library.INPUT[part])
        content.append('')
        # Section 5: Output
        content.extend(['*Output',
                        '*******',
                        '.print dc format=noindex file=' + output_filepath])
        content.extend(Library.OUTPUT[part][output_option])
        content.append('')
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
        if part == Library.PART_AD590:
            content.extend(['',
                            '*JFET',
                            '.model NJF_TYP NJF (',
                            '+ VTO = -1.0	BETA = 6.2E-4	LAMBDA = 0.003',
                            '+ RD = 0.01      RS = 1e-4',
                            '+ CGS = 3E-12    CGD=1.5E-12     IS=5E-10)',
                            '']),
        content.extend(['',
                        '*end of the netlist',
                        '.end'])
        
        # print content to netlist file
        file = open(netlist_filepath, 'wb')
        for line in content:
            text = (line + '\r\n').encode('ascii')
            file.write(text)
        file.close()
        return