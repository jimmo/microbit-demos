from neopixel import NeoPixel
from random import randint
from microbit import *

class Display:
  def __init__(self):
    self.row_en = [pin12,pin15,pin14,pin8,pin13,pin16]
    self.row_np = [
      NeoPixel(pin2, 30),
      NeoPixel(pin1, 30),
      NeoPixel(pin1, 30),
      NeoPixel(pin2, 30),
      NeoPixel(pin0, 30),
      NeoPixel(pin0, 30),
    ]
    for en in self.row_en:
      en.write_digital(1)

  def clear(self):
    for np in self.row_np:
      np.clear()

  def pixel(self, x, y, r, g, b):
    if x < 0 or y < 0 or x >= 30 or y >= 6:
      return
    self.row_np[y][29-x] = (r, g, b,)

  def draw(self):
    for ny in range(6):
      self.row_en[ny].write_digital(0)
      self.row_np[ny].show()
      self.row_en[ny].write_digital(1)

def rand_color():
  x = [randint(128, 255), randint(0, 128), randint(0, 128)]
  y = []
  for a in range(3):
    i = randint(0,len(x) - 1)
    y.append(x[i])
    x = x[:i] + x[i+1:]
  return y[0], y[1], y[2]

class Game:
  def __init__(self):
    self.x = 0
    self.y = 3
    self.t = 0
    self.o = []

  def explode(self, d):
    c = [[255, 0, 0], [244, 173, 66], [243, 241, 60]]
    for i in range(40):
      d.pixel(self.x + randint(-3, 3), self.y + randint(-3, 3), c[i%3][0], c[i%3][1], c[i%3][2])
      sleep(20)
      d.draw()
    self.x = 0
    self.y = 3
    self.t = 0
    self.o = []
    d.clear()

  def frame(self, d):
    d.clear()
    d.pixel(self.x, self.y, 255, 0, 0)
    d.pixel(self.x-1, self.y-1, 0, 255, 0)
    d.pixel(self.x+1, self.y-1, 0, 255, 0)
    d.pixel(self.x-1, self.y+1, 0, 255, 0)
    d.pixel(self.x+1, self.y+1, 0, 255, 0)
    for (x, h, r, g, b) in self.o:
      if h > 0:
        for y in range(h):
          d.pixel(x, y, r, g, b)
          if x == self.x and y == self.y:
            self.explode(d)
            return
      else:
        for y in range(-h):
          d.pixel(x, 5-y, r, g, b)
          if x == self.x and 5-y == self.y:
            self.explode(d)
            return
    d.draw()


    if self.t % 5 == 0:
      self.x = min(10, self.x + 1)
      o2 = []
      for i in range(len(self.o)):
        (x, h, r, g, b) = self.o[i]
        if x > 0:
          o2.append((x-1, h, r, g, b))
      self.o = o2
      if self.t % 15 == 0 and randint(0, 1):
        r, g, b = rand_color()
        self.o.append((29, randint(-4, 4), r, g, b))

    self.t += 1

    if button_a.was_pressed():
      self.y = max(0, self.y - 1)
    if button_b.was_pressed():
      self.y = min(5, self.y + 1)

g = Game()
d = Display()
while True:
  g.frame(d)
  sleep(40)
