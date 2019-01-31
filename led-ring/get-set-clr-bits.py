from microbit import *
from machine import mem8
display.off()

# outset bits:
# pin0, 0x50000508, 0x08
# pin1, 0x50000508, 0x04
# pin2, 0x50000508, 0x02
# pin3, 0x50000508, 0x10
# pin4, 0x50000508, 0x20
# pin10, 0x50000508, 0x40
# pin6, 0x50000509, 0x10
# pin7, 0x50000509, 0x08
# pin9, 0x50000509, 0x04
# pin8, 0x5000050a, 0x04
# pin12, 0x5000050a, 0x10
# pin13, 0x5000050a, 0x80
# pin14, 0x5000050a, 0x40
# pin15, 0x5000050a, 0x20
# pin16, 0x5000050a, 0x01

# clr bits:
# pin0, 0x5000050c, 0x08
# pin1, 0x5000050c, 0x04
# pin2, 0x5000050c, 0x02
# pin3, 0x5000050c, 0x10
# pin4, 0x5000050c, 0x20
# pin10, 0x5000050c, 0x40
# pin6, 0x5000050d, 0x10
# pin7, 0x5000050d, 0x08
# pin9, 0x5000050d, 0x04
# pin8, 0x5000050e, 0x04
# pin12, 0x5000050e, 0x10
# pin13, 0x5000050e, 0x80
# pin14, 0x5000050e, 0x40
# pin15, 0x5000050e, 0x20
# pin16, 0x5000050e, 0x01

base_addr = 0x50000000
outset_low = 0x508
outset_high = 0x50a
clr_low = 0x50c
clr_high = 0x50e

# outset register address
min_outset = base_addr+outset_low
max_outset = base_addr+outset_high

# clr register address
min_clr = base_addr+clr_low
max_clr = base_addr+clr_high

pins = [pin0, pin1, pin2, pin3, pin4, pin6, pin7, pin8, pin9, pin10, pin12, pin13, pin14, pin15, pin16]
lookup = {0:0, 1:1, 2:2, 3:3, 4:4, 5:6, 6:7, 7:8, 8:9, 9:10, 10:12, 11:13, 12:14, 13:15, 14:16}

# there must be a better way to get the pin number programatically...
def get_pin(pin):
  for idx, p in enumerate(pins):
    if p == pin:
      return lookup[idx]

# print the value if the register has changed
# the xor finds which bit has changed
def print_bits(addr):
  for p in pins:
    p.write_digital(0)
    x = mem8[addr]
    p.write_digital(1)
    y = mem8[addr]
    if x != y:
      print("pin{0}, 0x{1:x}, 0x{2:02x}".format(get_pin(p), addr, x^y))

print('outset bits:')
print('pin, addr, bit to set')
for addr in range(min_outset, max_outset+1):
  print_bits(addr)
print()
print('clr bits:')
print('pin, addr, bit to set')
for addr in range(min_clr, max_clr+1):
  print_bits(addr)