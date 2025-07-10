import socket

class SmartTrigPi():
    CHECK_COMMAND = '*IDN?\n'
    TRIG_COMMAND1 = '*TRG 4\n'
    TRIG_COMMAND2 = '*TRG 17\n'

    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT        

    def identify(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(self.CHECK_COMMAND.encode())
        self.ID = (self.s.recv(512))
        return self.ID
    
    def trigger1(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(self.TRIG_COMMAND1.encode())
        return self.s.recv(512)
    
    def trigger2(self):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(self.TRIG_COMMAND2.encode())
        return self.s.recv(512)
    
    def pulseWidth(self, pulseWidth):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(f'PULS:WIDT {pulseWidth}'.encode())
        return self.s.recv(512)

    def amplitude(self, amplitude):
        self.s = networkSetup(self.host, self.port)
        self.s.sendall(f'VOLT {amplitude}'.encode())
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