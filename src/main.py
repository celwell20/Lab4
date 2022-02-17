"""@file        main.py
   @brief       main file that runs pin step response
   @details     Runs voltage step response and records data using a timer interrupt
   @author        Clayton Elwell
   @author        Tyler McCue
   @date          February 10, 2022
"""

import pyb
import utime
import task_share

if __name__ == '__main__':
    
    ##Sets up pins for inputting signal and reading output
    pinA4 = pyb.Pin(pyb.Pin.cpu.C1, mode=pyb.Pin.OUT_PP)
    ## Sets up pin for ADC
    pinA5 = pyb.Pin(pyb.Pin.cpu.C0, mode=pyb.Pin.IN)

    ##Creates timer for interrupt 
    timer = pyb.Timer(1)
    timer.init(freq=1000)

    ##Creates share queue for data
    share = task_share.Queue('H', 1000, thread_protect=False, overwrite=False, name = "QQ")

    ##Creates ADC object from output pin
    adc = pyb.ADC(pinA5)
    
    def readPin(dummy):
        '''
        @brief              Reads pin value with ADC for interrupt
        '''
        share.put(adc.read(), in_ISR=True)

    
    pinA4.value(False)
    while True:
        ## Input received from serial port
        x = input()
        if x == "a":
            timer.callback(readPin)
            share.empty()
            pinA4.value(True)
        if x =="b":
            utime.sleep(0.5)
            timer.callback(None)
            print("start")
            while share.any():
                print(share.get())
            print("Done")
            pinA4.value(False)
        
