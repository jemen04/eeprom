#!/usr/bin/python

from smbus2 import SMBus, SMBusWrapper, i2c_msg
import time

with SMBusWrapper(1) as bus:
    
    address = 0x50          # 24LC256 i2c address - no address pins connected
    n_bytes = 8192          # 64k bits / (8bits/BYTES) = 8192 BYTES
    total_reg = 256
    my_list = []; temp = []

    # appends register address to list
    #for value in range(0, total_reg):
    #    a = bus.read_byte_data(address, value)
    #   my_list.append(hex(a))

    #print(my_list)
    #for i in range(0,100):
    #    b = bus.read_byte_data(address, 0xff)
    #    print(b)

    
    sentence = ""
    
    for value in range(0, n_bytes):
        b = bus.read_byte(address)
        b = chr(b)
        
        if b == '\xff':
            continue
        elif b == '\n':
            temp.append(sentence)
            sentence = ""
        else:
            sentence += b

    for words in temp:
        print(words)
    
