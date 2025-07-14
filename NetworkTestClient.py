from pymeasure.instruments.pi import smarttrigpi 
import time

def main():
    HOST = '146.136.47.129'
    PORT = 50007 #investigate if this really is the right port
    trigPi = smarttrigpi.SmartTrigPi(HOST, PORT)

    
    ID = trigPi.identify().decode()
    trigPi.amplitude = 5
    trigPi.pulseWidth = 0.000001
    time.sleep(.5)
    for i in range(10):
        trigPi.trigger()
       # trigPi.trigger2()

    print(ID)
    
if __name__ == "__main__":
    main()

