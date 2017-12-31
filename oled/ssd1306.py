from micropython import const
from microbit import i2c

SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)

class SSD1306():
    def __init__(self):
        self.buffer = bytearray(8 * 128 + 1)
        self.buffer[0] = 0x40
        self.temp = bytearray([0x80, 0])
        for cmd in (
            SET_DISP | 0x00,
            SET_MEM_ADDR, 0x00,
            SET_DISP_START_LINE,
            SET_SEG_REMAP | 0x01,
            SET_MUX_RATIO, 63,
            SET_COM_OUT_DIR | 0x08,
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xff,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CHARGE_PUMP, 0x10,
            SET_DISP | 0x01):
            self.cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.cmd(SET_DISP | 0x00)

    def poweron(self):
        self.cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.cmd(SET_CONTRAST)
        self.cmd(contrast)

    def invert(self, invert):
        self.cmd(SET_NORM_INV | (invert & 1))

    def fill(self, c):
      c |= (c << 4)
      c |= (c << 2)
      c |= (c << 1)
      for i in range(0, 128*8):
        self.buffer[i+1] = c

    def show(self):
        self.cmd(SET_COL_ADDR)
        self.cmd(0)
        self.cmd(127)
        self.cmd(SET_PAGE_ADDR)
        self.cmd(0)
        self.cmd(7)
        i2c.write(0x3c, self.buffer)

    def cmd(self, cmd):
        self.temp[1] = cmd
        i2c.write(0x3c, self.temp)
