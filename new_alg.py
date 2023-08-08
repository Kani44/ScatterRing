# run with:
# nc -l -u localhost 7355 | python3 new_alg.py

import sys
import numpy as np
import struct
import matplotlib.pyplot as plt
import argparse


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


parser = argparse.ArgumentParser()
parser.add_argument('on', type=str)
parser.add_argument('window', type=float)
parser.add_argument('slide', type=float)
parser.add_argument('gap', type=float)
parser.add_argument('--file', type=str)
parser.add_argument('--graph', action='store_true')
parser.add_argument('--realtime', action='store_true')

args = parser.parse_args()
ReadingType = args.on == 'True'
WindowSize = args.window
WindowSlide = args.slide
GapSize = args.gap
GraphOn = args.graph
RealTime = args.realtime
if not ReadingType:
    MyFile = args.file
else:
    MyFile = ''


class Source: 
    def __init__(self, online, fixednum, slidesize, gap, graph, realtime, filePath):
        self.cache = []
        self.graph = graph
        self.gap = gap
        self.fixednum = fixednum
        self.slidesize = slidesize
        self.sample_rate = 48000
        self.online = online
        self.realtime = realtime
        if self.online:
            pass
        else:
            self.file = open(filePath, 'r')
            print("File Opened")

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
            try:
                n = self.file.readline().rstrip()
                return(float(n))
            except ValueError:
                return(None)

    def collect(self):
        if self.graph:
            self.grapher = Grapher(self.slidesize, self.realtime)
            self.grapher.graphinit() #initialize 
        current_data = [] #the list of single lines of data read in through the getData function
        current_state = [] #the list of medians(maxlen 5)
        current_value = 0 #whether the most recently read median is a one or zero?
        first = True
        while True:
            value = source.getData()
            if value == None:
                break
            current_data.append(value)
            if len(current_data) >= int(self.fixednum * self.sample_rate):
                current_state, current_value, median, first = self.process(current_data, current_state, current_value, first)
                #time.sleep(0.1)
                if self.graph:
                    self.grapher.graph(median, current_value)
                current_data = []
        if self.graph: self.grapher.graphend()
        self.file.close()
        


    def process(self, data, state, last_value, first):

        med = np.median(data) #a single number
        #print(state)
        if first:
            if (med) < 0: #replace 0 with a number
                last_value = 1
            else:
                last_value = 0
            state = [med] #state is one median long
            
            first = False
        else: #not the first time
            if (len(state)>=1) and (abs(med-state[-1]) > self.gap) and (((last_value == 1) and ((med-state[-1]) < 0)) or ((last_value == 0) and ((med-state[-1]) > 0))):
                last_value = flip(last_value)
                #print(last_value)
                state = [med]
            else: #no last_value switch
                state.append(med)
                if len(state) == 5:
                    state = [med]
                    #print(last_value)
        
        return state, last_value, med, first

class Grapher:
    def __init__(self, slider, realtime):
        self.x_axis = []
        self.allvals = []
        self.slider = slider
        self.realtime = realtime
    
    def graph(self, medianValue, current_value):
        if medianValue.size > 0 :
            self.allvals.append(medianValue)
            self.x_axis.append(self.slider * (len(self.x_axis) + 1)) #keeps a running list of proper x-vals
            if current_value == 0:
                plt.title('ON', fontsize = 30, pad = 20)
            else:
                plt.title('OFF', fontsize = 30, pad = 20)
            if self.realtime:
                plt.plot(self.x_axis, self.allvals, color = 'black')
                plt.draw()
                plt.pause(0.001)

    def graphinit(self):
        plt.figure()
        plt.ion()
        if self.realtime:
            plt.show()
        plt.xlabel('Time (s)', fontsize = 15)
        plt.ylabel('Amplitude', fontsize = 15)
    
    def graphend(self):
        plt.ioff()
        if not self.realtime:
            plt.plot(self.x_axis, self.allvals, color = 'black')
        plt.show()

source = Source(ReadingType, WindowSize, WindowSlide, GapSize, GraphOn, RealTime, r'%s' % MyFile)

source.collect()