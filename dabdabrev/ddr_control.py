from microbit import *
import radio
import random

radio.config(channel=22)
radio.on()

NAMES = ['lw', 'ls', 'rw', 'rs']
coords = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
next_check = 0

#lw - 1: 200,700 up   x pos (right) x neg (left)
#     1: -200,-8000 down


#samp_sum = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
#samp_min = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
#samp_max = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
#samp_n = 0

IMAGES = [Image.ARROW_NE, Image.ARROW_NW, Image.ARROW_SE, Image.ARROW_SW]
CODES = ['--', '--', '++', '++']
c = 0

next = random.randint(0, 3)

while True:
    try:
        m = radio.receive()
    except:
        radio.off()
        radio.on()
        m = None
    if m:
        m = m.strip().split(':')
        if m[0] not in NAMES:
            continue
        i = NAMES.index(m[0])
        display.set_pixel(i, 0, 9)
        coords[i] = [float(m[1]), float(m[2]), float(m[3])]
    
    if running_time() > next_check:
        #print(coords)
        x = ''
        if coords[0][1] < 0:
            x += '+'
        else:
            x += '-'
            
        if coords[2][1] < 0:
            x += '+'
        else:
            x += '-'
        if x == CODES[next]:
            c += 1
            if c == 3:
                next = random.randint(0, 3)
                radio.send('lw:ding')
                radio.send('rw:ding')
                display.clear()
                sleep(1000)
                c = 0
        display.show(IMAGES[next])
        next_check = running_time() + 500
    