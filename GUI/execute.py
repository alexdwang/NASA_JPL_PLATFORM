import os
import subprocess

'''
execute system commands
'''
class Execute:
    # Create necessary directories and files if not exist
    def mkdirs(self):
        command = 'mkdir -p Database Output Library Library/temp'
        os.system(command)
        command = 'touch Library/library.json Library/name.json'
        os.system(command)
        return

    # remove all output files
    def rm_all(self):
        command = 'rm -f ./Output/*.txt'
        os.system(command)
        return

    # call Xyce to run simulations
    def execute_module3(self, path):
        # command = 'whereis bin/Xyce'# the command that going to be executed
        #Xyce_path = subprocess.getoutput(command)
        #command = Xyce_path.split(' ')[1] + ' ' + path  # the command that going to be executed
        # print(command)
        #result = subprocess.getoutput(command)
        # print(result)
        try:
            command = 'Xyce ' + path
            result = subprocess.call(command, shell=True, executable="/bin/tcsh")
        except:
            command = 'whereis bin/Xyce'    # find where is Xyce
            Xyce_path = subprocess.getoutput(command)
            command = Xyce_path.split(' ')[1] + ' ' + path  # the command that going to be executed
            result = subprocess.getoutput(command)
        return result

    # open a file from file system using default system application
    def open_file(self, path):
        command = 'xdg-open ' + path
        os.system(command)
        return