from smarttrigpi import SmartTrigPi
import time

def main():
    HOST = '146.136.32.49' #'146.136.47.129'
    PORT = 50007 #investigate if this really is the right port
    trigPi = SmartTrigPi(HOST, PORT)


    trigPi.reset()
    trigPi.output_load = 'INF'
    trigPi.shape = 'SQU'
    trigPi.square_period = 0.5
    trigPi.square_dutycycle = 70

    trigPi.amplitude = 5
    trigPi.frequency = 1
    trigPi.amplitude_unit = 'VPP'
    trigPi.offset = 2.5
    trigPi.burst_mode = 'TRIG'
    trigPi.burst_ncycles = 1  
    trigPi.trigger_source = "BUS"
    trigPi.burst_state = True
    trigPi.output = True
    
    trigPi.trigger()

    '''while True:
        trigPi.trigger()
        #trigPi.trigger1()
        time.sleep(1.5)'''
if __name__ == "__main__":
    main()

