import socket
import time

class SmartTrigPi():
    CHECK_COMMAND = '*IDN?\n'
    TRIG_COMMAND1 = '*TRG 17\n'
    TRIG_COMMAND2 = '*TRG 4\n'


    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
      
        self.amplitude = 5
        
        self.pulse_width = 0        
        self.frequency = 0               # Sets the output frequency to freq
        self.square_period = 0
        self.square_dutycycle = 0

        self.burst_state = True          # use burst mode for single trigger pulse
        self.burst_ncycles = 1           # one trigger pulse
        self.output_load = ''            # Error handling for backwards integration
        self.amplitude_unit = ''
        self.shape = ''              # Sets the output signal shape to a square wave
        self.offset = 0                # Sets the offset 
        self.output = ''               # Enables the output 
        self.trigger_source = '' 
   
    def setPulseWidth(self):
        self.s = networkSetup(self.host, self.port)
        if self.pulse_width and self.square_period:
            self.s.sendall(f'PULS:WIDT {self.pulse_width}'.encode())
            return self.square_period - self.pulse_width
        elif self.pulse_width and self.frequency:
            self.s.sendall(f'PULS:WIDT {self.pulse_width}'.encode())
            return 1/self.frequency - self.pulse_width
        elif self.square_dutycycle and self.square_period:
            self.pulse_width = self.square_period*(self.square_dutycycle/100)
            self.s.sendall(f'PULS:WIDT {self.pulse_width}'.encode())
            return self.square_period * (1-(self.square_dutycycle/100))
        elif self.square_dutycycle and self.frequency:
            self.pulse_width = self.square_period*(100/self.square_dutycycle)
            self.s.sendall(f'PULS:WIDT {self.pulse_width}'.encode())
            return self.square_period * (1-(100/self.square_dutycycle))

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
        delay = self.setPulseWidth()
        for i in range(self.burst_ncycles):
            self.s = networkSetup(self.host, self.port)
            self.s.sendall(self.TRIG_COMMAND1.encode())
            self.s.sendall(self.TRIG_COMMAND2.encode())
            time.sleep(delay)
        return self.s.recv(512)
    
    def trigger1(self):
        self.setAmplitude()
        delay = self.setPulseWidth()
        for i in range(self.burst_ncycles):
            self.s = networkSetup(self.host, self.port)
            self.s.sendall(self.TRIG_COMMAND1.encode())
            time.sleep(delay)
        return self.s.recv(512)
    
    def trigger2(self):
        self.setAmplitude()
        delay = self.setPulseWidth()
        for i in range(self.burst_ncycles):
            self.s = networkSetup(self.host, self.port)
            self.s.sendall(self.TRIG_COMMAND2.encode())
            time.sleep(delay)
        return self.s.recv(512)
    
    def close(self):
        return closeConnection(self.s)
    
    def write(self, message):
        print(f'{message}')
        return

    def reset(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall('*IDN?\n'.encode())
        time.sleep(.2)
        return

def networkSetup(host: str, port: int):
    s = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    return s

def closeConnection(s):
    s.close()