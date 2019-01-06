from microbit import *
import time

class LEDBar:
  def __init__(self, data, clk):
    self.data_pin = data
    self.clk_pin = clk
    self.values = []
    for i in range(10):
      self.values.append(0x0000)

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
      self.data_pin.write_digital((data & 0x80) >> 7)
      clk = 1 - clk
      self.clk_pin.write_digital(clk)
      data = data << 1

  def update(self):
    # send configuration
    self.send_data(0x0000)

    # send each LED
    for i in range(10):
      self.send_data(self.values[i])

    # send for two unconnected LEDs
    self.send_data(0x0000)
    self.send_data(0x0000)
    self.latch()

  def set_led(self, led, value):
    brightness = 2**value - 1
    if brightness < 0:
      brightness = 0
    if brightness > 255:
      brightness = 255
    self.values[led] = brightness


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
