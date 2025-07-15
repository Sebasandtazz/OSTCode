import smarttrigpi 
import time

def main():
    HOST = '146.136.47.129'
    PORT = 50007 #investigate if this really is the right port
    trigPi = smarttrigpi.SmartTrigPi(HOST, PORT)

    trigPi.burst_state = True
    trigPi.burst_ncycles = 10
    trigPi.output_load = 'INF'
    trigPi.shape = 'PULS'
    trigPi.amplitude = 5
    trigPi.pulse_width = 2e-3
    trigPi.offset = 2.5
    trigPi.frequency = 10
    trigPi.output = 'on'
    time.sleep(.5)
    
    trigPi.trigger()
    # trigPi.trigger2()

    
if __name__ == "__main__":
    main()

