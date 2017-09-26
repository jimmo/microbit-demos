from microbit import *
import radio

radio.config(channel=22)
radio.on()

def r():
  try:
    return radio.receive()
  except:
    radio.off()
    radio.on()
  return None

while True:
  m = r()
  if m:
    if int(m) > 28:
      music.pitch(440, 1000, wait=False)
    display.scroll(m)
