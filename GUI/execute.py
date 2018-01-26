import os
import subprocess

class Execute:
    def execute_module3(self):
        command = 'Xyce Netlist/test.cir'  # the command that going to be executed
        result = subprocess.getoutput(command)
        # print(result)
        return result