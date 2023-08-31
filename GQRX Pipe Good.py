import struct
import sys
import os

#nc -l -u localhost 7355 > GQRX Pipe.py

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, '')

def parse_signed_16bit_numbers(data):
    #Assuming 'data'is a 2-byte string or bytes object
    #Convert the bytes to a signed short using litte-endian format
    signed_number = struct.unpack('<h', data)[0]
    return signed_number

def split_by_2(string):
    return [parse_signed_16bit_numbers(string[i:i+2]) for i in range(0, len(string), 2)]


while True:
    print(split_by_2(sys.stdin))

with open("30.txt", 'r+b') as file:
    content = file.read()
    
new_data = split_by_2(content)
    
