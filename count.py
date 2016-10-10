import smbus
import time
bus = smbus.SMBus(0)
ADDRESS = 0x20 # address of MCP23017 (ground A0, A1, and A2)

def init():
    """configure appropraite outputs and inputs."""
    bus.write_byte_data(ADDRESS,0,255) # all is GPIO A input
    bus.write_byte_data(ADDRESS,1,0) # all is GPIO B output

def read():
    """read each of the four 8-bit registers."""
    vals=0
    for i,reg in enumerate([0b11111110,0b11111101,0b11111011,0b11110111]):
        bus.write_byte_data(ADDRESS,0x13,reg) # set GPIO B
        vals+=float(bus.read_byte_data(ADDRESS,18))*(256**i)
    return int(vals)
    
def readTwice():
    """only return a read if it's gotten twice."""
    while True:
        readA=read()
        readB=read()
        if readA==readB:
            return readA

if __name__=="__main__":
    init()
    readA=None
    while True:
        readB=readTwice()
        if readA is None:
            readA=int(readB)
        if readB==readA:
            continue
        diff = readB-readA
        if diff<0:
            diff+=2**32
        readA = int(readB)
        print("%.06f MHz"%(diff/1000000.0))
