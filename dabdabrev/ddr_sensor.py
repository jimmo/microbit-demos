from microbit import *
import music
import os
import radio

mode = None

if 'config' in os.listdir():
  f = open('config', 'rt')
  mode = f.read().strip()
  f.close()

if not mode or mode not in ('rw', 'rs', 'lw', 'ls',) or (button_a.is_pressed() and button_b.is_pressed()):
  mode = ''
  display.show('LR?', delay=200)
  while True:
    if button_a.was_pressed():
        mode += 'l'
        break
    if button_b.was_pressed():
        mode += 'r'
        break
  display.show('WS?', delay=200)
  while True:
    if button_a.was_pressed():
        mode += 'w'
        break
    if button_b.was_pressed():
        mode += 's'
        break
  f = open('config', 'wt')
  f.write(mode)
  f.close()

display.clear()
if mode == 'lw':
    display.set_pixel(0, 0, 9)
if mode == 'ls':
    display.set_pixel(0, 4, 9)
if mode == 'rw':
    display.set_pixel(4, 0, 9)
if mode == 'rs':
    display.set_pixel(4, 4, 9)

radio.config(channel=22)
radio.on()

while True:
    radio.send('{}:{}:{}:{}'.format(mode, accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()))
    try:
        m = radio.receive()
    except:
        radio.off()
        radio.on()
        m = None
    if m:
        m = m.split(':')
        if m[0] == mode:
            if m[1] == 'ding':
                music.play(music.BA_DING, wait=False)
            if m[1] == 'beep':
                music.pitch(440, 200, wait=False)
    sleep(100)
