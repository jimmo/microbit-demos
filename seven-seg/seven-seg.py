from microbit import *
from micropython import const
import time

TM1637_CMD1 = const(64)
TM1637_CMD2 = const(192)
TM1637_CMD3 = const(128)
TM1637_DSP_ON = const(8)
TM1637_DELAY = const(10)
_SEGMENTS = [63,6,91,79,102,109,125,7,127,111,119,124,57,94,121,113,0,64]

class TM1637(object):
    def __init__(self, clk, dio):
        self.clk = clk
        self.dio = dio
        time.sleep_us(TM1637_DELAY)
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def _start(self):
        self.dio.write_digital(0)
        time.sleep_us(TM1637_DELAY)
        self.clk.write_digital(0)
        time.sleep_us(TM1637_DELAY)

    def _stop(self):
        self.dio.write_digital(0)
        time.sleep_us(TM1637_DELAY)
        self.clk.write_digital(1)
        time.sleep_us(TM1637_DELAY)
        self.dio.write_digital(1)

    def _write_data_cmd(self):
        self._start()
        self._write_byte(TM1637_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        self._start()
        self._write_byte(TM1637_CMD3 | TM1637_DSP_ON | 7)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            self.dio.write_digital((b >> i) & 1)
            time.sleep_us(TM1637_DELAY)
            self.clk.write_digital(1)
            time.sleep_us(TM1637_DELAY)
            self.clk.write_digital(0)
            time.sleep_us(TM1637_DELAY)
        self.clk.write_digital(0)
        time.sleep_us(TM1637_DELAY)
        self.clk.write_digital(1)
        time.sleep_us(TM1637_DELAY)
        self.clk.write_digital(0)
        time.sleep_us(TM1637_DELAY)

    def write(self, segments, pos=0):
        if not 0 <= pos <= 3:
            raise ValueError("Pos")
        self._write_data_cmd()
        self._start()

        self._write_byte(TM1637_CMD2 | pos)
        for seg in segments:
            self._write_byte(seg)
        self._stop()
        self._write_dsp_ctrl()
        
    def encode_digit(self, digit):
        return _SEGMENTS[digit & 0x0f]

    def encode_string(self, string):
        segments = bytearray(4)
        for i in range(0, min(4, len(string))):
            segments[i] = self.encode_char(string[i])
        return segments

    def encode_char(self, char):
        o = ord(char)
        if o == 32:
            return _SEGMENTS[16]
        if o == 45:
            return _SEGMENTS[17]
        if o >= 65 and o <= 70:
            return _SEGMENTS[o-55]
        if o >= 97 and o <= 102:
            return _SEGMENTS[o-87]
        if o >= 48 and o <= 57:
            return _SEGMENTS[o-48]
        raise ValueError("Char")

    def hex(self, val):
        string = '{:04x}'.format(val & 0xffff)
        self.write(self.encode_string(string))

    def number(self, num):
        num = max(-999, min(num, 9999))
        string = '{0: >4d}'.format(num)
        self.write(self.encode_string(string))
t = TM1637(pin0, pin13)
    