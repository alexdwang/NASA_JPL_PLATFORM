from tkinter import *

class ValidatingEntry(Entry):
    # base class for validating entry widgets

    def __init__(self, master, value="", **kw):
        Entry.__init__(self, master, kw)
        self.__value = value
        self.__variable = StringVar()
        self.__variable.set(value)
        self.__variable.trace("w", self.__callback)
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(newvalue)
        else:
            self.__value = value

    def validate(self, value):
        # override: return value, new value, or None if invalid
        return value

# entry that only accept floats
class FloatEntry(ValidatingEntry):

    def validate(self, value):
        try:
            if len(value) == 1 and value == '-':
                return value
            elif len(value) > 1 and value[-1] == 'e':
                if (value[-2] == 'e' or value[-2] == '-'):
                    return None
                else:
                    return value
            elif len(value) > 2 and value[-1] == '-' and value[-2] == 'e':
                return value
            elif value:
                v = float(value)
            return value
        except ValueError:
            return None

# entry that accept TID level values (floats and float + k)
class TIDEntry(ValidatingEntry):

    def validate(self, value):
        try:
            if len(value) > 1 and value[-1] == 'k' and value.find('k', 0, len(value) - 1) == -1:
                # if float(value[0:-1]) > 300:
                #     return '300k'
                return value
            elif len(value) > 1 and value[-1] != 'k' and value.find('k') != -1:
                return None
            elif value:
                v = float(value)
                # if v > 300000:
                #     return '300000'
            return value
        except ValueError:
            return None
