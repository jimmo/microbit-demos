import microbit

# https://www.nxp.com/docs/en/data-sheet/PCF85063TP.pdf

RTC_ADDR = 0x51

PCF85063_REG_SC = 0x04

def bcd2bin(v):
    return v - 6 * (v >> 4)

def bin2bcd(v):
    return v + 6 * (v // 10)

def rtc_gettime():
    microbit.i2c.write(RTC_ADDR, bytes(PCF85063_REG_SC))
    data = microbit.i2c.read(RTC_ADDR, 8)
    # Ignore the first byte. TODO: Why?
    data = data[1:]
#    print("rtc_gettime:", " ".join(("%02x" % x) for x in data))
    ss = bcd2bin(data[0] & 0x7F)
    mm = bcd2bin(data[1])
    hh = bcd2bin(data[2])
    d = bcd2bin(data[4])
    m = bcd2bin(data[5])
    y = bcd2bin(data[6]) + 2000
    return [y, m, d, hh, mm, ss]

def rtc_settime(y, m, d, hh, mm, ss):
    data = []
    data.append(PCF85063_REG_SC)
    data.append(bin2bcd(ss))
    data.append(bin2bcd(mm))
    data.append(bin2bcd(hh))
    data.append(bin2bcd(0))
    data.append(bin2bcd(d))
    data.append(bin2bcd(m))
    data.append(bin2bcd(y - 2000))
#    print("rtc_settime:", " ".join(("%02x" % x) for x in data[1:]))
    microbit.i2c.write(RTC_ADDR, bytearray(data))

print("RTC Driver for micro:bit")

print(rtc_gettime())
