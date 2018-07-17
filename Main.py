import os
from GUI import Interface, reset

def relative_path(path):
    dirname = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(dirname, path)
    return os.path.normpath(path)


if __name__ == "__main__":
    interface = Interface.Interface()
    interface.start()

