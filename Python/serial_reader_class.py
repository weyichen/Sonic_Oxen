# A class that reads from the serial port using an isolated thread
class serial_reader_thread(threading.Thread):
    # Cookie-cutter __init__ function; nothing special
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.paused = False
    def on(self):
        return not self.paused
    def reset(self):
        # Print status and close port on exit
        self.paused = True
        print "Serial:", self.ser.inWaiting()
    def ready(self):
        # Make extra super sure we reset the Arduino
        while (self.ser.inWaiting()):
            self.ser.write("Stop!x")
            self.ser.flushInput()
            time.sleep(1)
        time.sleep(1)
        while (self.ser.inWaiting()):
            self.ser.write("Stop!x")
            self.ser.flushInput()
            time.sleep(1)
        time.sleep(1)
        while (self.ser.inWaiting()):
            self.ser.write("Stop!x")
            self.ser.flushInput()
            time.sleep(1)
        time.sleep(1)
        while (not self.ser.inWaiting()):
            self.ser.write("Begin!x")
            time.sleep(0.5)
        self.paused = False
    def run(self):
        self.ser = serial.Serial(4, baudrate=57600, timeout=1)
        self.ser.flushInput()
        self.ready()
        # Run until turned off
        while 1:
            if self.on():
                # Read bytes in chunks of meaningful size
                if self.ser.inWaiting() > 3:
                    b = bytearray(3)
                    self.ser.readinto(b)
                    # Don't read and write data simultaneously; acquire lock
                    dataLock.acquire()
                    data.append(b)
                    dataLock.release()