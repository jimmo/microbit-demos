import machine
import ssd1351
import amg8833
import random
import time

i = machine.I2C('Y')
a = amg8833.AMG8833(i, 0x68)
s = machine.SPI('Y')

d = ssd1351.SSD1351(128, 128, s, machine.Pin('Y4'), machine.Pin('Y3'), machine.Pin('Y5'))
d.fill(0)
d.show()

def rgb(r, g, b):
  r = min(r, 0xff) >> 3
  g = min(g, 0xff) >> 2
  b = min(b, 0xff) >> 3
  return (r << 11) | (g << 5) | b

def cell_color(t):
  return rgb(int(t * 255), 0, int((1-t) * 255))

def update(temp_data):
  temp_min = min(temp_data)
  temp_max = max(temp_data)
  temp_range = max(10, temp_max - temp_min)

  for x in range(8):
    for y in range(8):
      d.fill_rect((7-x) * 16, (7-y) * 16, 16, 16, cell_color((temp_data[x * 8 + y] - temp_min) / temp_range))

  d.text('{:.1f} - {:.1f}'.format(temp_min, temp_max), 5, 5, 0x0000)
  d.show()

try:
  while True:
    time.sleep_ms(100)
    update(a.capture())
except KeyboardInterrupt:
  pass
