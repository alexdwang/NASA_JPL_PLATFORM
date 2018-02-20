import os
import subprocess

class Execute:
    def mkdirs(self):
        command = 'mkdir Netlist Output FitCurve Library'
        os.system(command)
        command = 'touch Library/library.json Library/name.json'
        return

    def execute_module3(self, path):
        command = 'Xyce ' + path  # the command that going to be executed
        result = subprocess.getoutput(command)
        # print(result)
        return result