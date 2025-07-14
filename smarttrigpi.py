import socket

class SmartTrigPi():
    CHECK_COMMAND = '*IDN?\n'
    TRIG_COMMAND1 = '*TRG 4\n'
    TRIG_COMMAND2 = '*TRG 17\n'

    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.amplitude = 5
        self.pulseWidth = 0.25        

    def identify(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(self.CHECK_COMMAND.encode())
        self.ID = (self.s.recv(512))
        return self.ID
    
    def trigger(self):
        self.setAmplitude()
        self.setPulseWidth()
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(self.TRIG_COMMAND1.encode())
        return self.s.recv(512)
    
    def trigger2(self):
        self.setAmplitude()
        self.setPulseWidth()
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(self.TRIG_COMMAND2.encode())
        return self.s.recv(512)
    
    def setPulseWidth(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(f'PULS:WIDT {self.pulseWidth}'.encode())
        return self.s.recv(512)

    def setAmplitude(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(f'VOLT {self.amplitude}'.encode())
        return self.s.recv(512)
    
    def close(self):
        return closeConnection(self.s)

def networkSetup(host: str, port: int):
    s = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    return s

def closeConnection(s):
    s.close()