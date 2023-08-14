# run with:
# nc -l -u localhost 7355 | python3 new_alg.py

import sys
import numpy as np
import struct
import matplotlib.pyplot as plt
import pyautogui    
import argparse
import statistics as st
#import pyqtgraph as pg

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

def press_up():
    #pyautogui.keyDown('up')
    #print("Up key pressed")
    pass

def press_down():
    #pyautogui.keyDown('down')
    #print("Up key pressed")
    pass
   
def release():
    #pyautogui.keyUp('up')
    #pyautogui.keyUp('down')
    #print("Keys released")
    pass

def within(bound1, bound2, num, gap):
    bottom = 0
    top = 0
    if bound1 <= bound2:
        top = bound2
        bottom = bound1
    else:
        top = bound1
        bottom = bound2
    return (bottom + 0.3*gap) <= num <= (top - 0.3*gap)


parser = argparse.ArgumentParser()  
parser.add_argument('on', type=str)
parser.add_argument('window', type=float) 
parser.add_argument('slide', type=float)
parser.add_argument('gap', type=float)
parser.add_argument('--file', type=str)
parser.add_argument('--graph', action='store_true')
parser.add_argument('--realtime', action='store_true')
parser.add_argument('--debug', action='store_true')


args = parser.parse_args()
ReadingType = args.on == 'True'
WindowSize = args.window
WindowSlide = args.slide
GapSize = args.gap
GraphOn = args.graph
RealTime = args.realtime
DebugOn = args.debug
if not ReadingType:
    MyFile = args.file
else:
    MyFile = ''

class Data: 

    def __init__(self):
        self.data = []
        self.last = None
    
    def add(self, num): #append
        self.data.append(num)

    def reset(self, num): # = [med]
        self.data = [num] 
    
    def store(self): #last
        self.last = self.data[-2]
    
    def length(self): #len
        return len(self.data)
    
    def get(self, index): #[]
        return self.data[index]
    
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return str(self.data)
    
    def has_last(self):
        if self.last is None:
            return False
        else:
            return True



class Source: 
    def __init__(self, online, fixednum, slidesize, gap, graph, realtime, debug, filePath):
        self.graph = graph
        self.gap = gap
        self.fixednum = fixednum
        self.slidesize = slidesize
        self.sample_rate = 48000/129
        self.online = online
        self.realtime = realtime
        self.debug = debug
        if self.online:
            self.cache = []
        else:
            self.file = open(filePath, 'r')
            print("File Opened")

    def getData(self): #all one data point at a time
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
        current_data = []
        
        while True:
            value = source.getData() #a single number of data
            if value == None:
                break
            current_data = self.process(value, current_data)
        
        if self.graph: self.grapher.graphend()
        self.file.close()
        
    
    def process(self, value, data):
        if self.debug: print(value)
        if value > 12500:#___ * borderline:
            if len(data) > 0 and data[-1] > 0:
                data[-1] += 1
                if data[-1] >= 10: print(data[-1])
            else:
                data.append(1)
        elif value < 7500: #__ * borderline:
            if len(data) > 0 and data[-1] < 0:
                data[-1] -= 1
                if data[-1] <= -10: print(data[-1])
            else:
                data.append(-1)
        #print(data)
        if self.graph:
            self.grapher.graph(value, 'sure')
        return data


class Grapher:
    def __init__(self, slider, realtime):
        self.x_axis = []
        self.allvals = []
        self.slider = slider
        self.realtime = realtime
    
    def graph(self, medianValue, key):
        self.allvals.append(medianValue)
        self.x_axis.append(WindowSize + self.slider * (len(self.x_axis))) #keeps a running list of proper x-vals
        if key != None: 
            plt.title(key, fontsize = 30, pad = 20)
        if self.realtime:
            #pg.plot(self.x_axis, self.allvals, color = 'black')
            plt.plot(self.x_axis, self.allvals, color = 'black')
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
        plt.close()

source = Source(ReadingType, WindowSize, WindowSlide, GapSize, GraphOn, RealTime, DebugOn, r'%s' % MyFile)

source.collect()