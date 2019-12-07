# Write your code here :-)
from microbit import *

# Values for touch and release sensitivity
TOUCH_SENSITIVITY = 0xDD
RELEASE_SENSITIVITY = 0xAA

i2c.init()

# Initial register settings
registers = (
    (0x5E, 0x00), # ELE_CFG
    (0x2B, 0x01), # MHD_R
    (0x2C, 0x01), # NHD_R
    (0x2D, 0x00), # NCL_R
    (0x2E, 0x00), # FDL_R
    (0x2F, 0x01), # MHD_F
    (0x30, 0x01), # NHD_F
    (0x31, 0xFF), # NCL_F
    (0x32, 0x02), # FDL_F
    (0x41, TOUCH_SENSITIVITY), # ELE0_T
    (0x43, TOUCH_SENSITIVITY), # ELE1_T
    (0x45, TOUCH_SENSITIVITY), # ELE2_T
    (0x47, TOUCH_SENSITIVITY), # ELE3_T
    (0x49, TOUCH_SENSITIVITY), # ELE4_T
    (0x4B, TOUCH_SENSITIVITY), # ELE5_T
    (0x4D, TOUCH_SENSITIVITY), # ELE6_T
    (0x4F, TOUCH_SENSITIVITY), # ELE7_T
    (0x51, TOUCH_SENSITIVITY), # ELE8_T
    (0x53, TOUCH_SENSITIVITY), # ELE9_T
    (0x55, TOUCH_SENSITIVITY), # ELE10_T
    (0x57, TOUCH_SENSITIVITY), # ELE11_T
    (0x42, RELEASE_SENSITIVITY), # ELE0_R
    (0x44, RELEASE_SENSITIVITY), # ELE1_R
    (0x46, RELEASE_SENSITIVITY), # ELE2_R
    (0x48, RELEASE_SENSITIVITY), # ELE3_R
    (0x4A, RELEASE_SENSITIVITY), # ELE4_R
    (0x4C, RELEASE_SENSITIVITY), # ELE5_R
    (0x4E, RELEASE_SENSITIVITY), # ELE6_R
    (0x50, RELEASE_SENSITIVITY), # ELE7_R
    (0x52, RELEASE_SENSITIVITY), # ELE8_R
    (0x54, RELEASE_SENSITIVITY), # ELE9_R
    (0x56, RELEASE_SENSITIVITY), # ELE10_R
    (0x58, RELEASE_SENSITIVITY), # ELE11_R
    (0x5C, 0x10), # AFE1_CFG
    (0x5D, 0x04), # AFE2_CFG
    (0x80, 0X63), # RES_CF
    (0x5E, 0x8C), # ELE_CFG
)

def bit_read(i, b):
    return (i >> b) & 1

def write(address, data):
    i2c.write(0x5b, bytearray([address, data]))

def read_xy():
    '''Read x/y coordinates from the pad'''
    data = i2c.read(0x5b, 2)
    x = (data[0] & 0b11111)
    y = ((data[0] & 0b11100000) >> 1) | ((data[1] & 0b1111))
    return x, y

def keypad(var):
    '''Read a number from the numeric keypad'''
    if (var & 0x0001) > 0: return 1
    if (var & 0x0002) > 0: return 4
    if (var & 0x0004) > 0: return 7
    if (var & 0x0008) > 0: return 11

    if (var & 0x0010) > 0: return 2
    if (var & 0x0020) > 0: return 5
    if (var & 0x0040) > 0: return 8
    if (var & 0x0080) > 0: return 0

    if (var & 0x0100) > 0: return 3
    if (var & 0x0200) > 0: return 6
    if (var & 0x0400) > 0: return 9
    if (var & 0x0800) > 0: return 12


def setup():
    '''Push registers to controller'''
    for key, value in registers:
        write(key, value)
        print("Wrote {} = {}".format(key, value))

setup()

while True:
    # Assuming IRQ is plugged into pin2
    if not pin2.read_digital():
        data = i2c.read(0x5b, 2)

        key = keypad(data[1] << 8 | data[0])
        if key is not None:
            print(key)
            sleep(10)


'''
Other stuff that kinda works

def get_x():
    key = read()[0]
    a = bit_read(key, 0)
    b = bit_read(key, 1)
    c = bit_read(key, 2)
    d = bit_read(key, 3)
    e = bit_read(key, 4)
    if key > 0:
        if a == 1 and b != 1: return 1            # Electrode 0
        if a != 1 and b == 1 and c != 1: return 3  # Electrode 1
        if b != 1 and c == 1 and d != 1: return 5  # Electrode 2
        if c != 1 and d == 1 and e != 1: return 7  # Electrode 3
        if d != 1 and e == 1: return 9            # Electrode 4
        if a == 1 and b == 1: return 2            # Electrode 0 and 1
        if b == 1 and c == 1: return 4            # Electrode 1 and 2
        if c == 1 and d == 1: return 6            # Electrode 2 and 3
        if d == 1 and e == 1: return 8            # Electrode 3 and 4
    return -1;  # Release or other state

def get_y():
    key = read()[1];

    if key > 0:
        a = bit_read(key, 0)
        b = bit_read(key, 1)
        c = bit_read(key, 2)
        d = bit_read(key, 3)
        e = bit_read(key, 4)
        f = bit_read(key, 5)
        g = bit_read(key, 6)

        if a == 1 and b != 1: return 1              # Electrode 5
        if a != 1 and b == 1 and c != 1: return 3   # Electrode 6
        if b != 1 and c == 1 and d != 1: return 5   # Electrode 7
        if c != 1 and d == 1 and e != 1: return 7   # Electrode 8
        if d != 1 and e == 1 and f != 1: return 9   # Electrode 9
        if e != 1 and f == 1 and g != 1: return 11  # Electrode 10
        if f != 1 and g == 1: return 13             # Electrode 11
        if a == 1 and b == 1: return 2   # Electrode 5 and 6
        if b == 1 and c == 1: return 4   # Electrode 6 and 7
        if c == 1 and d == 1: return 6   # Electrode 7 and 8
        if d == 1 and e == 1: return 8   # Electrode 8 and 9
        if e == 1 and f == 1: return 10  # Electrode 9 and 10
        if f == 1 and g == 1: return 12  # Electrode 10 and 11
    return -1  # Release or other state

'''
