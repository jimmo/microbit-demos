from microbit import *
import radio

radio.config(channel=22)
radio.on()

while True:
  radio.send(str(temperature()))
  sleep(5000)
