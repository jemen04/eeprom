#! /usr/bin/env python3


import setuppath
import mfgtestfram2 as mfgtestfram

class EEPROM(mfgtestfram.IndividualTest):
	

    def setup(self):
        #'''initializes parameters and bus address'''
	print("Locating bus address")
