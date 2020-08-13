#
# Kenneth Shinn
# kshinn@sas.upenn.edu
#
# generate_signal.py
# This file contains the function to generate a signal given up to three indicators
#

class SignalGenerator:

    def __init__(self):
        pass

    def generate_signal(self, ind_1, ind_2 = None, ind_3 = None):
        return ind_1.dropna()