import serial

ser = serial.Serial(3, baudrate=57600, timeout=1)
print ser.inWaiting()
ser.setRTS(True) #?
ser.setRTS(False) #?
print ser.inWaiting()
ser.close()