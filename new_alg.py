import numpy as np
import struct
import sys


def parse_signed_16bit_numbers(data):
    #Assuming 'data'is a 2-byte string or bytes object
    #Convert the bytes to a signed short using litte-endian format
    signed_number = struct.unpack('<h', data)[0]
    return signed_number

def split_by_2(string):
    return [string[i:i+2] for i in range(0, len(string), 2)]




class Source: 
    sample_rate = 48000
    fixednum = .5
    slidesize = .5
    cache = []
    def __init__(self, online, filePath):
        self.online = online
        if online:
            pass
        else:
            self.file = open(filePath, 'r')

    def getData(self):
        if self.online:
            if len(self.cache) > 0:
                return self.cache.pop()
            else:
                data = sys.stdin.buffer.read(1024)
                new_data = split_by_2(data)
                for piece in new_data:
                    self.cache.append(parse_signed_16bit_numbers(piece))
                return self.cache.pop()
        else:
            return(self.file.readline())
            '''
            self.sumlists = []
            stuff = []
            for line in self.file:
                try:
                    stuff.append(float(line))
                except ValueError:
                    print(line)
                if len(stuff) >= self.sample_rate*self.fixednum:
                    self.sumlists.append(np.median(stuff))
                    '''


source = Source(False, r'C:\Users\ubicomplab\Downloads\sdrdataread\stuff.csv')
print(source.getData())

#def collect():
 #   while True:
        



            
            

