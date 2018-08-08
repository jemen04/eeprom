#!/usr/bin/python

from smbus2 import SMBus, SMBusWrapper
import time
import sys

with SMBusWrapper(1) as bus:
    address = 0x50
    register = 0
    #digit = 0
    data = [0]

    for value in range(0,10):
        data.append(value)
    
    bus.write_byte_data(address, 0, 8)
    
    #bus.write_i2c_block_data(address, register, data)
    #time.sleep(1)

    #byte = bus.read_byte_data(address, register)
    #print(byte)

    #sys.exit(0)
    byte = bus.read_i2c_block_data(address, 0, 16)
    print(byte)

    #byte = bus.read_byte_data(address, register)
    #print(byte)
    #byte = bus.read_byte_data(address, register)
    #print(byte)

    byte = bus.read_byte(address)
    print(byte)

    #my_list = []
    #for i in range(0,6000):
    #   my_list.append(bus.read_byte_data(address, register))
    #print(my_list)

    bus.write_i2c_block_data(address, register, data)
