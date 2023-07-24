import sys


def parse_signed_16bit_numbers(data):
    #Assuming 'data'is a 2-byte string or bytes object
    #Convert the bytes to a signed short using litte-endian format
    signed_number = struct.unpack('<h', data)[0]
    return signed_number

def split_by_2(string):
    return [string[i:i+2] for i in range(0, len(string), 2)]




class Source: 
    def __init__(self, online):
        self.online = online
        cache = []
        if online:
            pass
        else:
            filePath = #File Path
            file = open(filePath, 'r')

    def getData(self):
        if self.online:
            if len(cache) > 0:
                return cache.pop()
            else:
                data = sys.stdin.buffer.read(1024)
                new_data = split_by_2(data)
                for piece in data:
                    cache.append(parse_signed_16bit_numbers(piece))
                return cache.pop()
        else:
            sumlists = []
            while file.readable():
                #not yet ValueError proof because I want to try a list comprehension
                sumlist.append(median([float(file.readline()) for x in range(sample_rate * slidesize)]))


source = Source(True)

def collect():
    while True:
        



            
            

