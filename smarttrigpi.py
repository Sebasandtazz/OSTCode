import socket
import time

class SmartTrigPi():
    CHECK_COMMAND = '*IDN?\n'
    TRIG_COMMAND1 = '*TRG 4\n'
    TRIG_COMMAND2 = '*TRG 17\n'


    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.amplitude = 5
        self._pulse_width = 0.25        

        self.burst_state = True          # use burst mode for single trigger pulse
        self.burst_ncycles = 1           # one trigger pulse
        self.output_load = ''            # Error handling for backwards integration

        self.shape = ''              # Sets the output signal shape to a square wave
        self.frequency = 1               # Sets the output frequency to freq
        self.offset = 2.5                # Sets the offset 
        self.output = ''               # Enables the output 
        self.trigger_source = '' 

    @property
    def pulse_width(self):
        return self._pulse_width
    
    @pulse_width.setter
    def pulse_width(self,value):
        self._pulse_width = value
        self.setPulseWidth()
    

    def setPulseWidth(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(f'PULS:WIDT {self.pulse_width}'.encode())
        return self.s.recv(512)

    def setAmplitude(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(f'VOLT {self.amplitude}'.encode())
        return self.s.recv(512)


    def identify(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(self.CHECK_COMMAND.encode())
        self.ID = (self.s.recv(512))
        return self.ID
    
    def trigger(self):
        self.setAmplitude()
        self.setPulseWidth()
        for i in range(self.burst_ncycles):
            self.s = networkSetup(self.host, self.port)
            self.s.sendall(self.TRIG_COMMAND1.encode())
            time.sleep((1/self.frequency) - self.pulse_width)
        return self.s.recv(512)
    
    def trigger2(self):
        self.setAmplitude()
        self.setPulseWidth()
        for i in range(self.burst_ncycles):
            self.s = networkSetup(self.host, self.port)
            self.s.sendall(self.TRIG_COMMAND2.encode())
            time.sleep((1/self.frequency) - self.pulse_width)
        return self.s.recv(512)
    
    def close(self):
        return closeConnection(self.s)
    
    def write(self, message):
        print(f'{message}')
        return

def networkSetup(host: str, port: int):
    s = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    return s

def closeConnection(s):
    s.close()