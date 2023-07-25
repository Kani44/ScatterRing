# run with:
# nc -l -u localhost 7355 | python3 new_alg.py

import sys
from pynput import keyboard
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

def flip(value): 
    if value == 1:
        value = 0
    else:
        value = 1
    return value




class Source: 
    slidesize = .5
    def __init__(self, online, filePath):
    cache = []
    fixednum = .5
    sample_rate = 48000
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

def collect():
    window = 0.5
    current_data = []
    current_state = []
    x_axis = []
    allvals = []
    current_value = 0
    graphinit() #initialize 
    once = True
    while True:
        current_data.append(source.getData())
        if len(current_data) >= int(window*48000):
            current_data, current_state, current_value, median, once = process(current_data, current_state, current_value, once)
            graph(x_axis, median, allvals, current_value)


def process(data, state, last_value, first):
    gap = 50
    med = np.median(data)
    print(state)
    if first:
        if (med) < 0:
            last_value = 1
            print(last_value)
            state = [med]
            first = False
        else:
            last_value = 0
            print(last_value)
            state = [med]
            first = False
    else:

                            
        if (len(state)>=2) and (abs(med-state[-2])>gap):    # Next few lines append a 0.25 sec 1/0 depending on the average value of the previous sample
            if ((last_value == 1) and ((med-state[-2]) < 0)) or ((last_value == 0) and ((med-state[-2]) > 0)):
                last_value = flip(last_value)
                state = [med]
                print(last_value)
                print(state)
            else:
                state.append(med)
                if len(state) == 5: 
                    print(last_value)
                    state = [med]
        else:
            state.append(med)
            if len(state) == 5: 
                print(last_value)
                state = [med]
                #print(state)
    data = []
    return data, state, last_value, med, first

def graph(x_axis, medianValue, allvals, current_value):
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

def graphinit():
    plt.figure()
    plt.ion()
    plt.show()
    plt.xlabel('Time (s)', fontsize = 15)
    plt.ylabel('Amplitude', fontsize = 15)

collect()           
            

