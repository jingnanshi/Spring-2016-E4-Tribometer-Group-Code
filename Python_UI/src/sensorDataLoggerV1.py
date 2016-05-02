import os

#x = os.system("cat /dev/cu.usbmodem1411")


import serial
import datetime
import time

rpm = -1

def startup():
	'''
	Get them setup and ask for preferences
	'''

# syntax for reading from usb:
# 	ser = serial.Serial('/dev/cu.usbmodem1411', 9600) # open communication with the arduino
# 	while True:
#		print (ser.readline())

# syntax to write to arduino

def readAndWriteSensorData():
	print 'writing'
	dataFile = open('data2.txt', 'w') # open the file data.txt to write
	dataFile.write("Sensor Log starting at: ")
	dataFile.write(str(datetime.datetime.now()))
	ser = serial.Serial('/dev/cu.usbmodem1411', 9600) # open communication with the arduino

	timeout = time.time() + 5 # run for 5 seconds
	while time.time() < timeout:
	#while (ser.readline() != 'STOP'): # have the arduino send this to stop the trial
		stringIn = ser.readline()
		print (stringIn)
		floatsInString = [s for s in stringIn.split() if s[0].isdigit() or s[0] == '-'] # parse out the sensor value (kept as a string) from the serial prints
		print floatsInString
		# if there was an int in the string, find the first one and that's your sensor value
		if len(floatsInString) > 0:
			print 'writing to file'
			sensorValue = floatsInString[0]
			dataFile.write(sensorValue + '\n') # write to the file after turning it to a string
			dataFile.flush()
		#print (ser.readline())
	print "closing file"
	dataFile.close()

def writeStringToArduino(stringIn):
	'''
	Sends a string over serial to the arduino
	'''
	ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
	ser.write(stringIn)

def main():
	startup()
	readAndWriteSensorData()
	writeStringToArduino('500')

if __name__ == __main__:
    main()

# download serial libary: https://pypi.python.org/pypi/pyserial
'''
Download the archive from http://pypi.python.org/pypi/pyserial. Unpack the archive, enter the pyserial-x.y directory and run:

python setup.py install
'''

# stolen code

'''
## import the serial library
import serial

## Boolean variable that will represent 
## whether or not the arduino is connected
connected = False

## establish connection to the serial port that your arduino 
## is connected to.
'/dev/cu.usbmodem1411'
locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3', '/dev/cu.usbmodem1411']

for device in locations:
    try:
        print "Trying...",device
        ser = serial.Serial(device, 9600)
        break
    except:
        print "Failed to connect on",device

## loop until the arduino tells us it is ready
while not connected:
    serin = ser.read()
    connected = True

## open text file to store the current 
##gps co-ordinates received from the rover    
text_file = open("position4.txt", 'w')
## read serial data from arduino and 
## write it to the text file 'position.txt'
while 1:
    if ser.inWaiting():
        x=ser.read()
        print(x) 
        text_file.write(x)
        if x=="\n":
             text_file.seek(0)
             text_file.truncate()
        text_file.flush()

## close the serial connection and text file
text_file.close()
ser.close()


'''
