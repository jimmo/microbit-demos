from microbit import *
import time

b = bytearray(13*2*2)

def set_level(n, l):
  if n >= 12:
    n += 1
  b[(n + 1) * 2 + 1] = l

@micropython.asm_thumb
def send_byte(r0):
  # r1 pointing to the GPIO base addr
  mov(r1, 0x50)       # r0=0x50
  lsl(r1, r1, 16)     # r0=0x500000
  add(r1, 0x05)       # r0=0x500005
  lsl(r1, r1, 8)      # r0=0x50000500

  # Mask for the clock pin (pin0)
  mov(r7, 0x08)       # pin0 is 0b00001000 in the first byte

  # Get the existing value of byte containing pin13
  ldrb(r3, [r1, 6])   # r3=existing pin13
  mov(r4, 0x80)       # p13 is 0b10000000 (conveniently the high bit)
  bic(r3, r4)         # clear pin13 bit

  # Mask to clear all bits other than the high bit.
  mov(r4, 0x7f)
  # Amount to shift left by.
  mov(r6, 1)

  # Loop counter.
  mov(r2, 4)
  label(LOOP)
  
  mov(r5, r0)         # copy r0...
  bic(r5, r4)         # ...and clear all other bits
  orr(r3, r5)         # copy high bit from r5 into r3
  strb(r3, [r1, 6])   # store back r3 to GPIO
  lsl(r0, r6)         # shift left r0
  str(r7, [r1, 8])    # set clk
  
  mov(r5, r0)         # as above
  bic(r5, r4)
  orr(r3, r5)
  strb(r3, [r1, 6])
  lsl(r0, r6)
  str(r7, [r1, 12])   # clr clk

  # Stop after four iterations.
  sub(r2, 1)
  bne(LOOP)
  

def update():
  pin13.write_digital(0)
  pin0.write_digital(0)
  
  for i in b:
    send_byte(i)
    
  time.sleep_us(200)

  for i in range(9):
    pin13.write_digital(i & 1)

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
