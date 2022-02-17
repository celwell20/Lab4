"""@file        UI.py
   @brief       UI for pin step response file
   @details     Displays UI and communicates to stm board through the serial port
   @author        Clayton Elwell
   @author        Tyler McCue
   @date          February 10, 2022
"""
import serial as s
import matplotlib.pyplot as plt
import time

class UI:
    '''!
    User interface task that allows us to start a step response and plot the data
    '''
    
    def __init__(self, com):
        '''
        @brief      Constructor for user interface
        @param com  com. name used to connect to stm through serial port
        '''
        ## COM port attribute
        self.comnum = com
        
        print(' ______________________________ ')
        print('|                              |')
        print('|  Welcome to the C.T. UI      |')
        print('|  Commands:                   |')
        print('|     A. Start Step Response.  |')
        print('|     B. Print Data            |')
        print('|______________________________|')
        print('\n')
    
    
    def run(self, command):
        '''
        @brief              Send message through serial port
        @param command      Command being sent
        '''
        with s.Serial(str(self.comnum), 115200) as port:
            port.write((command+"\r\n").encode('utf-8'))
    
    def read(self):
        '''
        @brief              Reads data sent from stm using start and stop markers
        '''
        flag = True
        x = [] #preallocating some lists for future storage
        y = []
        with s.Serial(str(self.comnum), 115200) as port:
            appStrt = False
            while flag:
                try:
                    data = port.readline().decode('utf-8')
                    if appStrt:
                        cooked = data.replace('\r\n', '')
                        y.append(int(cooked)) #adding first index to x list
                    if "start" in data:
                        appStrt = True
                except:
                    break
                    
            plt.plot(y)
            plt.xlabel('Time (ms)')
            plt.ylabel('Voltage (ADC Read)')
            plt.title('Step Response of Pin')
            plt.show()
                    
if __name__ == '__main__':
    ## User interface module object
    user = UI('/dev/tty.usbmodem207C337057522')
    while True:
        ## Keyboard input storage variable
        c = 0
        c = input("Enter Command: ")
        user.run(c)
        if c == "a":
           print("Setting pin to high!")
        elif c == "b":
            user.read()
