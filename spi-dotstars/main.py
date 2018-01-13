# SPI dotstars
# NCSS 2018 Summer School
# Authors: Sofia, Owen, Moss

from microbit import *

N_PIXELS = 15


def write_frames(frames):
    spi.write(bytes(frames))

def rgb_to_frames(rgb):
    frames = [0]*4

    for r, g, b in rgb:
        frames += [0b11111111, b, g, r]

    frames += [0xff]*4

    return frames

def main():
    spi.init(baudrate=1000000,mosi=pin13,sclk=pin0)

    rgb = [(255, 0, 0),
           (0, 255, 0),
           (0, 0, 255),
           (255, 0, 0),
           (0, 255, 0),
           (0, 0, 255),
           (255, 0, 0),
           (0, 255, 0),
           (0, 0, 255),
           (255, 0, 0),
           (0, 255, 0),
           (0, 0, 255)]

    frames = rgb_to_frames(rgb)
    write_frames(frames)

if __name__ == '__main__':
    main()
