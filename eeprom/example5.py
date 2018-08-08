from smbus2 import SMBus, SMBusWrapper, i2c_msg
import time
address = 0x50
regmsbyte = 00
reglsbyte = 00

with SMBusWrapper(1) as bus:
    #bus.write_byte_data(address, regmsbyte, reglsbyte)
    #exit()
    #bus.write_byte(address, 00)

    chars = bus.read_i2c_block_data(address, 0,32)
    print('starting:', chars, len(chars))
    for i in range(len(chars)):
        c = chars[i]
        print('{} {:8b} {:2x} {}'.format(i+1, c, c, repr(chr(c))[1:-1] ))
        
    datalsbyte = bus.read_byte(address)
    datamsbyte = bus.read_byte(address)

    print('\nsecond:')
    bus.write_byte_data(address, regmsbyte, reglsbyte)
    for i in range(96):
        b = bus.read_byte(address)
        print('{} {:8b} {:2x} {}'.format(i+1, b, b, repr(chr(b))[1:-1] ))
        #print('{:2x} {:2x}'.format(bus.read_byte(address), bus.read_byte(address)))
        #print(hex(bus.read_byte(address)), hex(bus.read_byte(address)))

    writestring = [35, ord('X')]
    #print(writestring)
    bus.write_i2c_block_data(address, regmsbyte, writestring)


def write(dev_add, start_add, strings):
    address = dev_add
    start_add_ms = start_add & 0xFF00
    start_add_ls = start_add & 0x00FF

    print('--\n{:8b}'.format(start_add_ls))

    data = [start_add_ls]
    for char in strings[:32]:
        data.append(ord(char))


    data = data[:32]
    print('data:', data)
    with SMBusWrapper(1) as bus:
        time.sleep(0.1)
        bus.write_i2c_block_data(address, start_add_ms, data)
    
#write(0x50,1, '?Amazing!')
#write(0x50,0, '1234567890ABCDEFGHIKLMNabcdefghik')


# reset offset
with SMBusWrapper(1) as bus:
    time.sleep(0.1)
    bus.write_byte_data(address, regmsbyte, reglsbyte)
    #bus.write_byte(address, 00)
