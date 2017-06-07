from microbit import *
import radio

radio.on()
radio.config(channel=28)

display.show(Image.BUTTERFLY * 0.2)

while True:
  try:
    if button_a.was_pressed():
      radio.send('a')
    if button_b.was_pressed():
      radio.send('b')
  except:
    radio.off()
    radio.on()
