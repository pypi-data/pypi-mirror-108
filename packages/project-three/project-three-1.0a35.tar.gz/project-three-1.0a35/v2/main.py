# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pkg_resources

pkg_resources.require("numpy==1.19")  # modified to use specific numpy

import numpy as npVs


class Pepe():
    def print_hi(name):
        # Use a breakpoint in the code line below to debug your script.
        print(f'Soy la version de numpy, {npVs.__version__}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    p = Pepe
    p.print_hi('asd')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
