#!/usr/bin/python

from smbus2 import SMBus, SMBusWrapper
import time
import os
import sys

address = 0x50          #24LC64 i2C address - A0, A1, A2 N/A Grounded
n_bytes = 8192          #64Kb/(8b/1B) = 8192B
start_pos = 0           #Most Significant


def read(dev_add=address, start_add=start_pos):
    ''' Returns a list of eeprom data read, within the normal ascii range (0-126)'''

    with SMBusWrapper(1) as bus:

        eeprom_data = []                                #Holds read eeprom data
        bus.write_byte_data(address, 0,0)

        for value in range(start_add, n_bytes):         #Iterates through memory
            eeprom_data.append(bus.read_byte(address))  #Appends read byte

        sentences = ascii2_char(eeprom_data)            #converts bytes to chr equiv
        
        return sentences                                


def read_all():
    '''Reads all eeprom data and returns list as ascii code'''
    
    with SMBusWrapper(1) as bus:
        data = []                                       #Holds read eeprom data
        bus.write_byte_data(address, 0,0)               

        for value in range(n_bytes):                    #Iterates through memory
            data.append(bus.read_byte(address))
        return data



def read_file(file_name):
    '''Reads a file, and returns a formated list of accepted char '''
    
    try:

        size = os.path.getsize(file_name)               #Gets file size of file

        if size > n_bytes - 256:                        #checks file sizes
            print("size of file is to big, please limit to 8192 Bytes")
            sys.exit(9)

        my_file = open(file_name, "r")                  #Reads file

        return char2_ascii(my_file)                      

    except Exception as e:
        raise


def write(dev_add, start_add, my_list):
    data = []
    

    with SMBusWrapper(1) as bus:
        bus.write_byte_data(address, 0, 0)

        for start_addr in range(len(my_list)):

            

            if start_addr % 32 == 0 and start_addr > 0:
                
                lsbyte = start_addr & 0x00FF
                msbyte = start_addr >> 8

                #print(data)
                #import pdb; pdb.set_trace()
                
                writestring = [lsbyte] + data[0:len(data)-1]
                #print(writestring, len(writestring))
                bus.write_i2c_block_data(address, msbyte, writestring)
                time.sleep(0.1)

                current = (start_addr - 1) + 32
                clsbyte = current & 0x00FF
                cmsbyte = current >> 8
                #print(current, clsbyte, cmsbyte, chr(data[len(data)-1]) )
                
                writestring = [clsbyte] + [data[len(data)-1]]
                #print(writestring, len(writestring))
                #import pdb; pdb.set_trace()
                
                bus.write_i2c_block_data(address, cmsbyte, writestring)
                time.sleep(0.1)
                data = []

            data.append(my_list[start_addr])
                    


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
    ascii_values = []
    for sentence in string_data:
        for char in sentence:
            ascii_values.append(ord(char))

    return ascii_values


def factory_reset(active=False):
    '''Resets ALL memory, use with caution '''

    if active == True:                                  #Safety, user must trigger
        #print("Reseting EEPROM: ETA 40.95 seconds")

        with SMBusWrapper(1) as bus:
            bus.write_byte_data(address, 0, 0)

            for start_addr in range(n_bytes):           
                if start_addr % 32 == 0:

                    current = 31 + start_addr
                    clsbyte = current & 0x00FF
                    cmsbyte = current >> 8
                    
                    lsbyte = start_addr & 0x00FF
                    msbyte = start_addr >> 8
                    writestring = [lsbyte] + [255]*31

                    bus.write_i2c_block_data(address, msbyte, writestring)
                    time.sleep(0.1)
                    bus.write_i2c_block_data(address, cmsbyte, [clsbyte, 255])
                    time.sleep(0.1)
                    #print('---0x{:4x} {}'.format(start_addr, start_addr))
                    #print('lo 0x{:4x} {}'.format(lsbyte, lsbyte))
                    #print('hi 0x{:4x} {}'.format(msbyte, msbyte))

    else:
        print("factory activity status set to false, no changes!")
#############################################################################
#############################################################################


d = read_file('/home/semap/Desktop/eeprom/input.txt')
factory_reset(True)                    #Resets eeprom
        
write(0x50,0, d)

print(read())                           #returns readable eeprom data as list
#print(read_all())                      #returns all eeprom data as list
