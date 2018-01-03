from microbit import *
import time

#Array of states of the LEDs
states = []
for i in range(10):
    states.append(0x0000)

def latch():
    pin0.write_digital(0)
    time.sleep_us(500)
    for i in range(4):
        pin0.write_digital(1)
        pin0.write_digital(0)


def send_data(data):
    clk = 0
    for i in range(16):
        pin0.write_digital((data & 0x8000) >> 15)
        clk = 1-clk
        pin13.write_digital(clk)
        data <<= 1
        


def set_data(states):
    #This sets the configuration data
    send_data(0x0000)
    #This sets the state of each LED (i.e. the brightness)
    for i in range(10):
        send_data(states[i])
    #This is empty bits for the two unconnected LEDs
    send_data(0x0000)
    send_data(0x0000)
    
    latch()

growing = True
wait = True
state = 0
while True:
    if button_a.was_pressed():
        wait = False
        growing = True
    if button_b.was_pressed():
        wait = False
        growing = False
    if growing == True and wait == False:
        states[state] += 10000
        if states[state] >= 0xFFFF:
            state += 1
        if state == 10:
            state = 9
            wait = True
    elif growing == False and wait == False:
        states[state] -= 10000
        if states[state] <= 0x0000:
            state -= 1
        if state == -1:
            state = 0
            wait = True
    set_data(states)
        
    
    