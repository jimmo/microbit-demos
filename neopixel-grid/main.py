from neopixel import NeoPixel
from random import randint
from microbit import *


n0 = NeoPixel(pin0, 30) # 4,5
n1 = NeoPixel(pin1, 30) # 1,2
n2 = NeoPixel(pin2, 30) # 0,3
row_en = [pin12,pin15,pin14,pin8,pin13,pin16]
row_np = [n2,n1,n1,n2,n0,n0]

for en in row_en:
  en.write_digital(1)

class Game:
  def __init__(self):
    self.x = 0
    self.y = 3
    self.t = 0

  def pixel(self, x, y):
    if self.t < 0:
      if randint(0,2) == 0:
        return (randint(0,255), randint(0,255), randint(0,255),)
      else:
        return (0,0,0,)
    if x == self.x and y == self.y:
      return (255, 0, 0,)
    if abs(x - self.x) == 1 and abs(y - self.y) == 1:
      return (0, 255, 0,)
    else:
      return (0, 0, 0,)

  def frame(self):
    sleep(20)
    if self.t < 0:
      return
    self.t += 1
    self.x = (self.t) % 30
    if button_a.is_pressed() and button_b.is_pressed():
      self.t = -1
      return
    if button_a.was_pressed():
      self.y -= 1
    if button_b.was_pressed():
      self.y += 1

g = Game()
while True:
  for ny in range(6):
    row_en[ny].write_digital(0)
    for nx in range(30):
      row_np[ny][nx] = g.pixel(29-nx, ny)
    row_np[ny].show()
    row_en[ny].write_digital(1)
  g.frame()
