# This function runs grouping on data and graphs the result

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from tqdm import tqdm

rel_path = sys.argv[1]
fixednum = float(sys.argv[2])
slidesize = float(sys.argv[3])

def split_by(list, fixednum, slidesize, sample_rate):
    fixednum = int(fixednum*sample_rate)
    slidesize = int(slidesize*sample_rate)
    new = [np.mean(list[i:i+fixednum]) for i in range(0, len(list), slidesize)]
    return new

name = rel_path #this is just a holdover for incase the name should be changed
spec_path = name+".csv"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, spec_path) # for this to work files should be in the same folder

sample_rate = 48000

sumList = []
data = []

with open(abs_file_path, 'r') as file:
    for i in tqdm(range(int(os.path.getsize(abs_file_path) / (2*sample_rate*slidesize*5)))): #how many bytes per line?
        file.seek(i*sample_rate*slidesize*5) #slide it over - don't ask about the *5
        for j in range(int(sample_rate * fixednum)):
            try:
                data.append(float(file.readline()))#read that amount into a list
            except ValueError:
                pass
        sumList.append(np.mean(data))


time = np.linspace(0, len(sumList)/sample_rate, np.size(sumList))

plt.plot(time, sumList)
plt.title('Time Domain Signal'  + '(' + str(fixednum) + ', ' + str(slidesize) + ')')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.savefig(script_dir + '/Images/' + name + '(' + str(fixednum) + ', ' + str(slidesize) + ')' + 'groupedtime.jpg') #save
plt.show()
plt.close()
plt.figure()