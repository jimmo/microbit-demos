from microbit import *


class Encoder:

  def __init__(self, pin_a, pin_b):
    self.x = 0
    self.old_sig_a = False
    self.sig_a = 0
    self.sig_b = 0
    self.pin_a = pin_a
    self.pin_b = pin_b
    self.setup_pins(pin_a, pin_b)

  def setup_pins(self, pin_a, pin_b):
    pin_b.read_digital()
    pin_b.set_pull(pin_b.PULL_UP)
    pin_a.read_digital()
    pin_a.set_pull(pin_a.PULL_UP)

  def read_rotor(self):
    self.sig_a = self.pin_a.read_digital()
    self.sig_b = self.pin_b.read_digital()
    if self.sig_a and not self.old_sig_a:
      if self.sig_b:
        self.x += 1
      else:
        self.x -= 1
    if self.x > 9:
      self.x = 0
    elif self.x < 0:
      self.x = 9
    self.old_sig_a = self.sig_a
    return self.x


rotor = Encoder(pin2, pin15)

while True:
  x = rotor.read_rotor()
  display.show(str(x))
  sleep(5)
