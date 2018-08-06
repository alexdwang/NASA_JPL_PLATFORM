import os
from GUI import Interface, reset


# get relative path to the program folder
def relative_path(path):
    dirname = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(dirname, path)
    return os.path.normpath(path)

# main function, call Interface to start the program
if __name__ == "__main__":
    interface = Interface.Interface()
    interface.start()

