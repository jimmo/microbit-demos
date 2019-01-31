from microbit import *
import time

class LEDBar:
  def __init__(self, data, clk):
    self.data_pin = data
    self.clk_pin = clk
    self.values = []
    for i in range(10):
      self.values.append(0)

  def latch(self):
    self.clk_pin.write_digital(0)
    self.data_pin.write_digital(0)
    time.sleep_us(500)
    for i in range(4):
      self.data_pin.write_digital(1)
      self.data_pin.write_digital(0)

  def send_data(self, data):
    clk = 0

    # write MSB as 8 zeros
    for i in range(8):
      self.data_pin.write_digital(0)
      clk = 1 - clk
      self.clk_pin.write_digital(clk)

    # write data
    for i in range(8):
      self.data_pin.write_digital((data >> 7) & 1)
      clk = 1 - clk
      self.clk_pin.write_digital(clk)
      data = data << 1

  def update(self):
    # send configuration
    self.send_data(0x0000)

    # send each LED
    for v in self.values:
      self.send_data(v)

    # send for two unconnected LEDs
    self.send_data(0)
    self.send_data(0)
    self.latch()

  def set_led(self, led, value):
    if led > len(self.values) - 1:
      return
    brightness = 2**value - 1
    if brightness < 0:
      brightness = 0
    elif brightness > 255:
      brightness = 255
    self.values[led] = brightness

  def clear(self):
    for led in range(10):
      self.values[led] = 0
    self.update()

bar = LEDBar(pin0, pin13)
while True:
  for led in range(10):
    for i in range(9):
      bar.set_led(led, i)
      bar.update()
  for led in range(9, -1, -1):
    for i in range(8, -1, -1):
      bar.set_led(led, i)
      bar.update()
