from smarttrigpi import SmartTrigPi 
import time

def main():
    HOST = '146.136.47.129'
    PORT = 50007 #investigate if this really is the right port
    trigPi = SmartTrigPi(HOST, PORT)

    
    ID = trigPi.identify().decode()
    print(trigPi.amplitude(5).decode())
    print(trigPi.pulseWidth(0.000001).decode())
    time.sleep(.5)
    for i in range(2000):
        trigPi.trigger1()
        trigPi.trigger2()

    print(ID)
    
if __name__ == "__main__":
    main()

