import serial
import time

ser = serial.Serial()
ser.port = 'COM12'
ser.baudrate = 9600
ser.open ()

while 1:
	read = ser.inWaiting()
	print (ser.read(read))	
	time.sleep (1)	