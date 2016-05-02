import serial
import sys
import glob
import time
import serial.tools.list_ports
import signal

posSignal = 'p' # a character to put on front of the signal so the arduino knows what to do with it
rpmSignal = 'r'

def writeStringToArduino(stringIn, arduinoName):
    '''
    Sends a string over serial to the arduino
    '''
    #start a timer in case it takes too long
    def handler(signum, frame):
        print "raising time exception"
        raise Exception("end of time")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10) 
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
