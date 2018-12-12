from microbit import *
import time
import machine

b = bytearray(13*2)

def set_level(n, l):
  l = ((l >> 1) & 1) | ((l >> 2) & 2) | ((l >> 3) & 4) | ((l >> 4) & 8)
  
  if n >= 12:
    n += 1
  b[(n + 1)] = l

def update():
  spi.init(baudrate=100000, bits=8, mode=0, sclk=pin0, mosi=pin13, miso=None)
  spi.write(b)
  
  # spi1->enable = 0
  machine.mem8[0x40004500] = 0

  # pin 13 = 0
  machine.mem8[0x5000050e] |= 0b10000000
  for i in range(4):
    # pin13 = 1
    machine.mem8[0x5000050a] |= 0b10000000
    # pin13 = 0
    machine.mem8[0x5000050e] |= 0b10000000

while True:
  for i in range(24):
    set_level((i + 21) % 24, 0)
    set_level((i + 22) % 24, 2)
    set_level((i + 23) % 24, 10)
    set_level((i + 24) % 24, 255)
    set_level((i + 25) % 24, 10)
    set_level((i + 26) % 24, 2)
    set_level((i + 27) % 24, 0)
    update()
    sleep(10)
