import sys
import numpy as np
import struct
import matplotlib.pyplot as plt
import pyautogui 
#from pylab import *
from rtlsdr import *
import heapq
from matplotlib.mlab import psd

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

MyFile = sys.argv[1]
WindowSize = float(sys.argv[2])
WindowSlide = float(sys.argv[3])
GapSize = float(sys.argv[4])
frequency = 64.00109375

class Data: 

    def __init__(self):
        self.datas = []
        self.last = None
    
    def add(self, num):
        self.datas.append(num)

    def reset(self, num):
        self.datas = [num]
    
    def store(self):
        self.last = self.datas[-2]
    
    def length(self):
        return len(self.datas)
    
    def get(self, index):
        return self.datas[index]
    
    def __str__(self):
        return str(self.datas)
    
    def __repr__(self):
        return str(self.datas)
    
    def has_last(self):
        if self.last is None:
            return False
        else:
            return True

class Source: 
    def __init__(self, online, fixednum, slidesize, gap, filePath, freq):
        self.cache = []
        self.gap = gap
        self.fixednum = fixednum
        self.slidesize = slidesize
        self.sample_rate = 48000
        self.online = online
        self.freq = freq
        if self.online:
            self.sdr = RtlSdr()
            # configure device
            self.sdr.sample_rate = 1.8e6
            self.sdr.center_freq = 63.98e6
            self.sdr.gain = 0
            
        else:
            self.file = open(filePath, 'r')
            print("hi")

    def getData(self):
        if self.online:
            samples = self.sdr.read_samples(256*1024)
            Pxx, freqs = psd(samples, NFFT=1024, Fs=self.sdr.sample_rate/1e6)
            freqs += self.sdr.center_freq/1e6 
            points = dict(zip(freqs, Pxx))
            return points.get(self.freq)
        else:
            return(int(self.file.readline())) #seems to always be an int

    def collect(self):
        current_data = Data() #the list of single lines of data read in through the getData function #the list of medians(maxlen 5)
        current_decode = []
        x_axis = []
        allvals = []
        current_value = 0 #whether the most recently read median is a one or zero?
        self.graphinit() #initialize 
        first = True
        while True:
            
            
        
            current_data, current_value, median, current_decode, first = self.process(current_data, current_value, current_decode, first)
            self.graph(x_axis, median, allvals, current_value)
            
                
            


    def process(self, data, last_value, decode, first):
        
         #a single number
        
        med = source.getData()
       
        print(data)
        
        if first:
            if (med) < 0: #replace 0 with a number
                last_value = 1
            else:
                last_value = 0
            data.reset(med) #state is one median long
            
            first = False
            decode.append(last_value)
           
        else: #not the first time
            if data.length() == 1 and data.has_last() and within(data.last, med, data.get(0), self.gap) and (abs(med-data.last)>self.gap):
                print("hikhjkljhjklkljhgfldkjhaldhfankljdhlusadfhadfs;jadslisadfhilusdf") #if state is one long and has 2nd to last value and 1st and 3rd values have a gap and the gap between 2nd and 3rd values is fairly large
                data.reset(med)
                last_value = flip(last_value)
                if last_value == 1:
                    press_up()
                else:
                    release()
            elif (data.length()>=2) and (abs(med-data.get(-2)) > self.gap) and (((last_value == 1) and ((med-data.get(-2)) < 0)) or ((last_value == 0) and ((med-data.get(-2)) > 0))):
                last_value = flip(last_value)
                print(last_value)
                decode.append(last_value)
                data.reset(med)
                # if decode == [1,1]:
                #     press_up()
                #     decode = []
                # elif decode == [0,0]:
                #     press_down()
                #     decode = []
                # elif len(decode) >= 2:
                #     release()
                #     decode = []
                # else:
                #     pass
                if last_value == 1:
                    press_up()
                else:
                    release()
            else: #no last_value switch
                data.add(med)
                if data.length() == 4:
                    data.store()
                    data.reset(med)
                    print(last_value)
                    decode.append(last_value)
                    # if decode == [1,1]:
                    #     press_up()
                    #     decode = []
                    # elif decode == [0,0]:
                    #     press_down()
                    #     decode = []
                    # elif len(decode) >= 2:
                    #     release()
                    #     decode = []
                    # else:
                    #     pass
                    if last_value == 1:
                        press_up()
                    else:
                        release()
        
        return data, last_value, med, decode, first

    def graph(self, x_axis, medianValue, allvals, current_value):
        if medianValue.size > 0 :
            allvals.append(medianValue)
            x_axis.append(0.5 * (len(x_axis) + 1)) #keeps a running list of proper x-vals
            plt.plot(x_axis, allvals, color = 'black')
            if current_value == 1:
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

source = Source(True, WindowSize, WindowSlide, GapSize, r'%s' % MyFile, 64.00109375)

source.collect()