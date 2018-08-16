#! /usr/bin/env python3

import setuppath
import json

from smbus2 import SMBus, SMBusWrapper
import mfgtestfram2 as mfgtestfram


class EEPROM_24LC64(mfgtestfram.IndividualTest):


    #def __init__(self):                        #Initialize Variables
    #    self.bus_address = address
    #    self.n_bytes = 8192
    #    super().__init__()

    def setup(self):                                    #Will locate bus address
        '''initializes parameters and bus address'''    
        print("Locating bus address")
        limit1 = self.limits
        print(limit1)

    def run_test(self):
        
        limit1 = self.limits
        print(limit1)

    
    def read_all_ascii(self):
        '''Reads all eeprom data and returns list as ascii code'''

        with SMBusWrapper(1) as bus:
            data = []                                       #Holds read eeprom data
            address = self.bus_address
            bus.write_byte_data(address, 0,0)               #Starting location

            for value in range(self.n_bytes):               #Iterates through memory
                data.append(bus.read_byte(address))         #Returns ALL data read
            return data                                     #as list of ascii codes

                        


if __name__ == '__main__':

    runable = mfgtestfram.Runnable()
    runable.load_available_tests([EEPROM_24LC64])
    runable.get_options_cli()
    #runable.start_equip_client()
    runable.initialize()
    runable.run()
    runable.finalize()


    #runnable = EEPROM_24LC64(0x50)
    #runnable.setup()
