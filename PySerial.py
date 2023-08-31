import serial #from the pyserial library, not the serial library 
import sys
import time

start = sys.argv[1]
portnum = 'COM12' #Port that Arduino is in, look at bottom right of IDE 

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))

arduino = serial.Serial(port=portnum, baudrate=115200, timeout=.1)
time.sleep(2)
write_read(start)
while True:
    start = input("Value: ")
    write_read(start)