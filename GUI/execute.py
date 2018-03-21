import os
import subprocess

class Execute:
    def mkdirs(self):
        command = 'mkdir -p Netlist Output FitCurve Library Library/temp'
        os.system(command)
        command = 'touch Library/library.json Library/name.json'
        os.system(command)
        return
    
    def rm_all(self):
        command = 'rm -f ./Output/*'
        os.system(command)
        return

    def execute_module3(self, path):
        command = 'Xyce ' + path  # the command that going to be executed
        result = subprocess.getoutput(command)
        # print(result)
        return result
