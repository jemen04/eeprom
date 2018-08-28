#! /usr/bin/env python3

import setuppath
import json

from smbus2 import SMBus, SMBusWrapper
import mfgtestfram2 as mfgtestfram


class EEPROM_24LC64():

    def __init__(self, address):                       #Initialize Variables
        self.bus_address = address
        self.n_bytes = 8192

    def read_all_ascii(self):
        '''Reads all eeprom data and returns list as ascii code'''

        with SMBusWrapper(1) as bus:
            data = []                                   #Holds read eeprom data
            address = self.bus_address
            bus.write_byte_data(address, 0, 0)          #Starting location

            for value in range(self.n_bytes):           #Iterates through memory
                data.append(bus.read_byte(address))     #Returns ALL data read
            return data                                 #as list of ascii codes

    def read(self):
        ''' Returns a char list of eeprom data read, within ascii range (0-126)'''

        eeprom_data = EEPROM.read_all_ascii()           #Returns all eeprom data found
        sentences = EEPROM.ascii2_char(eeprom_data)     #converts values to character
        
        return sentences                                #Returns list of characters

    def read_file(self, file_name):
        '''Reads a file, and returns a formated list of accepted char '''
    
        try:
            size = os.path.getsize(file_name)               #Gets file size of file

            if size > self.n_bytes - 256:                   #checks file sizes
                print("size of file is to big, please limit to 8192 Bytes")
                sys.exit(9)

            my_file = open(file_name, "r")                  #Reads file
            return char2_ascii(my_file)                     #Returns ascii

        except Exception as e:
            raise
        
    def write_memory(self, d_dict):
        '''Recieves a dictionary with write address as key and data as value'''
        address = self.bus_address                          #address to eeprom
        
        with SMBusWrapper(1) as bus:
            bus.write_byte_data(address, 0, 0)              #signals start
            
            for start_add, data in d_dict.items():          #iterates through key and value pairing
                current_add = int(start_add)                #converts key to integer
                writestring = __blocks(data)                #breaks current data into blocks up to 32 bytes
                
                for i in range(len(writestring)):

                    lsbyte = (current_add + i*32) & 0x00FF  #Least significant bytes of current address
                    msbyte = (current_add + i*32) >> 8      #Most significant bytes of current address
                    cls = (current_add - 1 + i*32) + 32     #Current address of last byte
                    clsbyte = cls & 0x00FF                  #LS of last byte in block
                    cmsbyte = (current_add + i*32) >> 8     #MS of last byte in block

                    if len(writestring[i]) == 32:
                        c_block = [lsbyte] + writestring[i][0:len(writestring) - 1]
                        bus.write_i2c_block_data(address, msbyte, c_block)
                        time.sleep(0.1)
                                                 
                        c_block = [clsbyte] + writestring[i][len(writestring)]
                        bus.write_i2c_block_data(address, cmsbyte, c_block)
                        time.sleep(0.1)
                    else:
                        c_block = [lsbyte] + writestring[i][0:len(writestring)]
                        bus.write_i2c_block_data(address, msbyte, c_block)

    def __blocks(string_data):
        '''Returns a list of list of up to 32 bytes per list'''
        my_blocks  = []                                     #main block that is returned
        temp_block = []                                     #stores up to 32 bytes

        for char in string_data:                            #iterates through all data
            temp_block.append(char)                         #filling up block
            
            if len(temp_block) == 32:                       #block is full move to main block
                my_blocks.append(temp_block)                #appends list of 32 bytes to main block
                temp_block = []                             #reset for next bytes
            
        if len(temp_block) != 0:                            #Last block may not have 32 bytes
            my_blocks.append(temp_block)                    #appends remaining to main list

        return temp_block
        
    def factory_reset(self, active=False):
        '''Resets ALL memory, use with caution '''

        if active == True:                                  #Safety, user must trigger
            #print("Reseting EEPROM: ETA 40.95 seconds")

            with SMBusWrapper(1) as bus:
                bus.write_byte_data(address, 0, 0)          #Starting Location

                for start_addr in range(n_bytes):           #Erasing all bytes      
                    if start_addr % 32 == 0:                #32 Bytes a block
                        current = 31 + start_addr           #Position of 32nd byte
                        clsbyte = current & 0x00FF
                        cmsbyte = current >> 8
                            
                        lsbyte = start_addr & 0x00FF        #position of 1st 31 bytes
                        msbyte = start_addr >> 8
                        writestring = [lsbyte] + [255]*31   #Start byte and erase bytes

                        bus.write_i2c_block_data(address, msbyte, writestring)
                        time.sleep(0.1)
                        bus.write_i2c_block_data(address, cmsbyte, [clsbyte, 255])
                        time.sleep(0.1)
        else:
            print("factory activity status set to false, no changes!")

    def ascii2_char(list_data):
        '''Function that converts a list of ascii to char '''
        data = []
        words = ""

        for i in range(0, len(list_data)):                  #iterates through data
            if 0<= list_data[i] <= 126:                     #ascii range (0-126)
                if list_data[i] == 10 and len(words) != "": #newline found append sentence
                    data.append(words)
                    words = ""
                else:                                       #regular char, build sentence
                    words += chr(list_data[i])                  
            if i == len(list_data)-1 and words != "":       #end of file, add sentence
                data.append(words)
        return data

    def char2_ascii(string_data):
        '''Function that converts list of chr to ascii '''
        ascii_values = []                                   #holds list of ascii values
        for sentence in string_data:                        #Reads line by line
            for char in sentence:                           #Reads characters in line
                ascii_values.append(ord(char))              #appends ascii value
        return ascii_values


class Program24LC64(mfgtestfram.IndividualTest):
    name = "EEPROM Test 24LC64"
    test_version = '1.0'
    default_failure_code = 'EEP-100'

    def run_test(self):
        self.run_one(run_number=1)

    def run_one(self, run_number=1):
        self.result.passed = self.eeprom_test()

    def eeprom_test(self):                                  #Kraken Eeprom Test       
        data = self.limits['data']
        byte_limit = 32        

        my_bus = self.limits['bus']
 
        for i in range(len(data)):
            key = list(data[i].keys())
            val = data[i].get(key.pop())
            
            if len(val) > byte_limit:                       #Checks data limit 
                self.result.add_error_code('KEKE-104')      
                return False

        if len(self.result.test_failures) == 0:
            return True
    
    def read_eeprom_rules(self):
        json_file = open('rules_eeprom.json')
        json_str = json_file.read()
        json_data = json.loads(json_str)
        return json_data

    def dut_reserved_keys(self,input_dic):
        return input_dic['reserved'].keys()

    def key_2_size(self, my_keys, my_dict):
        my_list = []
        for key in my_keys:
            check_type = my_dict['reserved'][key]            
            if type(check_type) is dict:
                my_list.append(my_dict['reserved'][key]['size'])
            else: 
                my_list.append([32])
        return my_list

if __name__ == '__main__':

    runable = mfgtestfram.Runnable()
    runable.load_available_tests([Program24LC64])
    runable.get_options_cli()
    #runable.start_equip_client()
    runable.initialize()
    runable.run()
    runable.finalize()
