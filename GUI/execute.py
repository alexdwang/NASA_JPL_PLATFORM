import os
import subprocess

class Execute:
    def mkdirs(self):
        command = 'mkdir Netlist Output FitCurve'
        os.system(command)
        return

    def execute_module3(self, path):
        command = 'Xyce ' + path  # the command that going to be executed
        result = subprocess.getoutput(command)
        # print(result)
        return result