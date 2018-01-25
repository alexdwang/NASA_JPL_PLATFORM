import os
import subprocess

class Execute:
    def execute_module3(self):
        command = 'Xyce Netlist/LT1175_Prerad_LineRegulation_V12.cir'  # the command that going to be executed
        result = subprocess.getoutput(command)
        # print(result)
        return result
        pass
