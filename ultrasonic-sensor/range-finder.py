'An example range-finder using a ultrasonic sensor and the 25 leds'

from microbit import *
import machine
import time

TRIGGER = pin0
ECHO = pin1
ECHO.read_digital()
ECHO.set_pull(ECHO.NO_PULL)

def read_distance_cm(trigger_pin, echo_pin):
    '''
    Get distance in cm from an object using HC-SR04 ultrasonic sensor.
    The sensor requires 5V in (doesn't operate properly on 3v).
    Use voltage divider to lower ECHO signal to 3v.
    Use a delay of at least 60ms between calls to read_distance.
    '''
    trigger_pin.write_digital(0)
    time.sleep_us(2)
    trigger_pin.write_digital(1)
    time.sleep_us(10)
    trigger_pin.write_digital(0)
    time.sleep_us(10)
    # 60000us timeout (max about 400cm). A larger timeout will make it possible to detect larger distances
    pw = machine.time_pulse_us(echo_pin, 1, 60000) 
    if pw < 0:
        # No full pulse detected before timeout
        return None
    else:
        # Divide by 58 to get centimetres as per spec
        return pw/58

while True:
    # Read the distance and colour a number of leds proportional to the distance (from 0 to 200cm)
    d = read_distance_cm(TRIGGER, ECHO) or 400
    leds = 25*min(d/200, 1.0)
    image = Image(''.join(''.join(str(9 if y*5+x < leds else 0) for x in range(5)) + ':' for y in range(5)))
    display.show(image)
    sleep(60)
