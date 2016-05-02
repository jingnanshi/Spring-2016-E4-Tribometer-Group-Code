import serial
import sys
import glob
import time
import serial.tools.list_ports
import signal

posSignal = 'p' # a character to put on front of the signal so the arduino knows what to do with it
rpmSignal = 'r'

<<<<<<< Updated upstream
def writeStringToArduino(stringIn, arduinoName):
=======

def readAndWriteSensorData(name):
    '''
    Given a name for the arduino (its usb string) read data from it until it sends a stop command, or times out
    '''
    print 'writing'
    dataFile = open('data2.txt', 'a') # open the file data.txt to write - 'a' for append, so won't overwrite old results
    dataFile.write("Sensor Log starting at: ")
    dataFile.write(str(datetime.datetime.now()))
    ser = serial.Serial(name, 9600) # open communication with the arduino

    # setup the timer
        def handler(signum, frame):
        print "raising time exception"
        raise Exception("end of time")
    signal.signal(signal.SIGALRM, handler)
  
    stringIn = ''
    while (stringIn != 'STOP'): # have the arduino send this to stop the trial

        signal.alarm(10) # setup the timer to wait 10 seconds before timing out
        try:
            stringIn = ser.readline()
            floatsInString = [s for s in stringIn.split() if s[0].isdigit() or s[0] == '-'] # parse out the sensor value (kept as a string) from the serial prints
            # if there was an int in the string, find the first one and that's your sensor value
            if len(floatsInString) > 0:
                print 'writing to file'
                sensorValue = floatsInString[0]
                dataFile.write(sensorValue + '\n') # write to the file after turning it to a string
                dataFile.flush()
            #print (ser.readline())
        except Exception:
            print 'arduino took too long to send data'
            break  # if it errors, break out of this
    print "closing file"
    dataFile.close()
    signal.alarm(0)


def writeStringToArduino(stringIn):
>>>>>>> Stashed changes
    '''
    Sends a string over serial to the arduino
    '''
    #start a timer in case it takes too long
    def handler(signum, frame):
        print "raising time exception"
        raise Exception("end of time")
    signal.signal(signal.SIGALRM, handler)
<<<<<<< Updated upstream
    signal.alarm(10) 
=======
    signal.alarm(10)
    ports = list(serial.tools.list_ports.comports())
    name = ""
    for p in ports:
        if 'Arduino' in p[1]:
            name = p[0]
>>>>>>> Stashed changes
    try:
        
        ser = serial.Serial(arduinoName, 9600)
        ser.write(stringIn)

        stringIn = ser.readline()
        print("Response: ")
        print stringIn
    except Exception:
        print 'arduino took too long to respond, threw exception'

    # end that timer
    signal.alarm(0)

def convertDistToArduino(amount):
    '''
    Change to the units used in the arduino positioning
    '''
    return amount * 500 # ARBITRARY FIGURE THIS OUT TO CALIBRATE 

def changePos(amount,arduinoName):
    '''
    Send a signal to the arduino to change the position by a given amount
    format: posSignal followed by the amount as a string 
    '''
    print("Changing by: ")
    print(amount)
    distToSend = convertDistToArduino(amount)
    stringToSend = posSignal + formatNum(5, distToSend) # make sure to tag on the signal to let the arduino know what to do
    print "Sending:"
    print stringToSend
    writeStringToArduino(stringToSend,arduinoName)

def setRPM(rpm,arduinoName):
    '''
    Send a signal to the arduino to set the rpm - 
    format: rpmSignal followed by the number as a string
    '''
    stringToSend = rpmSignal + formatNum(5, rpm)
    writeStringToArduino(stringToSend,arduinoName)

def formatNum(endLength, amount):
    '''
    take a number and tag on leading zeros to it - return as a string - also have the first digit correspond to pos or negative
    ex: -120 --> 1000120

    1 represents negative
    '''
    amountAsStr = str(amount)
    if amountAsStr[0] == '-': 
        amountAsStr = amountAsStr[1:] # peel off the negative sign if need be
    numZeros = endLength - len(amountAsStr) - 1 # the extra one for the sign bit
    if numZeros < 0:
        print "ERROR - not a long enough string to fit it all!"
    else:
        if amount < 0:
            return '1' + '0' * numZeros + amountAsStr
        else:
            return '0' + '0' * numZeros + amountAsStr

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def getArduinoPort():
    """ get the port connecting to arduino
    """
    ports = list(serial.tools.list_ports.comports())
    name = ""
    for p in ports:
        if 'Arduino' in p[1]:
            name = p[0]
    return name
