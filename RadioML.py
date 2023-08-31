#The cool grapher

import Lister
import numpy as np
import sys
import matplotlib.pyplot as plt

def splitter(lst, sec):
    size = int(sec*48000)
    temp = [np.median(lst[i:i+size]) for i in range(0, len(lst), size)]
    temp.pop()
    return temp

def check_overlap(range1, range2):
    # range1 and range2 are lists representing the ranges (min, max)
    return (range1[1] >= range2[0] and range2[1] >= range1[0])


amplitudes = []
labels = []

#pretty self-explanatory ngl
nameOn = sys.argv[1] + '.txt'
nameOff = sys.argv[2] + '.txt'
windowincrement = float(sys.argv[3])
numwindows = int(sys.argv[4])



on = Lister.txt_to_lst(nameOn)
off = Lister.txt_to_lst(nameOff)

def window_changer(sec):
    
    #sec = round(sec, 5)
    off_array = splitter(off, sec)
    on_array = splitter(on, sec)
    return([min(off_array), max(off_array), min(on_array), max(on_array)])


window_lengths = np.linspace(windowincrement, numwindows*windowincrement, num=numwindows)
print(window_lengths)

minmaxlist = []
for time in window_lengths:
    minmaxlist.append(window_changer(time))
minmaxlist = np.transpose(minmaxlist)
offmins = minmaxlist[0]
offmaxes = minmaxlist[1]
onmins = minmaxlist[2]
onmaxes = minmaxlist[3]

diffoff = [offmaxes[i] - offmins[i] for i in range(len(offmaxes))]
diffon = [onmaxes[i] - onmins[i] for i in range(len(onmaxes))]
gap = [0 if offmins[i] - onmaxes[i] < 0 else offmins[i] - onmaxes[i] for i in range(len(onmaxes))] 

plt.bar(window_lengths, diffoff, bottom = offmins, width = windowincrement/2, align = 'edge', color = 'blue')
plt.bar(window_lengths, diffon, bottom = onmins, width = windowincrement/2, align = 'edge', color = 'orange')
plt.bar(window_lengths, gap, bottom = onmaxes, width = windowincrement/2, align = 'edge', color = 'red')
plt.show()
