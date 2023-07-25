# run with:
# nc -l -u localhost 7355 | python3 new_alg.py

import sys
import numpy as np
import struct
import matplotlib.pyplot as plt


def parse_signed_16bit_numbers(data):
    #Assuming 'data'is a 2-byte string or bytes object
    #Convert the bytes to a signed short using litte-endian format
    signed_number = struct.unpack('<h', data)[0]
    return signed_number

def split_by_2(string):
    return [string[i:i+2] for i in range(0, len(string), 2)]

'''
def flip(value): 
    if value == 1:
        value = 0
    else:
        value = 1
    return value
'''

MyFile = sys.argv[1]

class Source: 
    def __init__(self, online, filePath):
        self.cache = []
        self.fixednum = .5
        self.slidesize = .5
        self.sample_rate = 48000
        self.online = online
        if self.online:
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
            return(int(self.file.readline())) #seems to always be an int

    def collect(self):
        current_data = []
        current_state = []
        x_axis = []
        allvals = []
        current_value = 0
        self.graphinit() #initialize 
        once = True
        while True:
            current_data.append(source.getData())
            if len(current_data) >= int(self.fixednum*48000):
                current_data, current_state, current_value, median, once = self.process(current_data, current_state, current_value, once)
                self.graph(x_axis, median, allvals, current_value)


    def process(self, data, state, last_value, first):
        gap = 50
        med = np.median(data)
        if first:
            if (med) < 0:
                last_value = 1
                state = [med]
                first = False
            else:
                last_value = 0
                state = [med]
                first = False
        else:
            if (len(state)>=2) and (abs(med-state[-2])>gap):    # Next few lines append a 0.25 sec 1/0 depending on the average value of the previous sample
                
                if ((last_value == 1) and ((med-state[-2]) < 0)) or ((last_value == 0) and ((med-state[-2]) > 0)):
                    last_value = flip(last_value)
                    state = [med]
                else:
                    state.append(med)
                    if len(state) == 5: 
                        state = [med]
            else:
                state.append(med)
                if len(state) == 5:
                    state = [med]
        data = []
        return data, state, last_value, med, first

    def graph(self, x_axis, medianValue, allvals, current_value):
        if medianValue.size > 0 :
            allvals.append(medianValue)
            print('med', medianValue)
            x_axis.append(0.5 * (len(x_axis) + 1))
            plt.plot(x_axis, allvals, color = 'black')
            if current_value == 0:
                plt.title('ON', fontsize = 30, pad = 20)
            else:
                plt.title('OFF', fontsize = 30, pad = 20)
            plt.draw()
            plt.pause(0.001)

    def graphinit(self):
        plt.figure()
        plt.ion()
        plt.show()
        plt.xlabel('Time (s)', fontsize = 15)
        plt.ylabel('Amplitude', fontsize = 15)


source = Source(False, r'%s' % MyFile)

source.collect()           
            

