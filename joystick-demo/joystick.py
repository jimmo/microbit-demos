from microbit import *


def lerp(x, y_min, y_max, x_min=0, x_max=1):
    '''
    Linear Interpolation between two ranges.
    Maps x linearly from [x_min, x_max] to [y_min, y_max]
    '''
    return (x - x_min) / (x_max - x_min) * (y_max-y_min) + y_min

class Joystick:
    def __init__(self, pin_x, pin_y):
        self.DELTA = 255
        self.RANGE = 100
        self.x = pin_x
        self.y = pin_y
        self.calibrate_centre()
        self.x_min = self.x_mid - self.DELTA
        self.x_max = self.x_mid + self.DELTA
        self.y_min = self.y_mid - self.DELTA
        self.y_max = self.y_mid + self.DELTA
    
    def calibrate_centre(self, x = None, y = None, auto = True):
        if auto:
            self.x_mid = self.x.read_analog()
            self.y_mid = self.y.read_analog()
        else:
            self.x.default = x
            self.y.default = y
    
    def calibrate_range(self):
        self.x_min = self.x_mid
        self.x_max = self.x_mid
        self.y_min = self.y_mid
        self.y_max = self.y_mid
        start = running_time()
        display.show(Image.ALL_CLOCKS, delay=100, loop=True, wait=False)
        while running_time() - start < 5000:
            cur_x = self.x.read_analog()
            cur_y = self.y.read_analog()
            self.x_max = max(self.x_max, cur_x)
            self.x_min = min(self.x_min, cur_x)
            self.y_max = max(self.y_max, cur_y)
            self.y_min = min(self.y_min, cur_y)
        display.show(Image.YES)
    
    def read(self, raw=False):
        cur_x = self.x.read_analog()
        cur_y = self.y.read_analog()
        if not raw:
            if cur_x > self.x_mid:
                scale_x = lerp(cur_x, 0,100, self.x_mid, self.x_max) 
            else:
                scale_x = lerp(cur_x, -100, 0, self.x_min, self.x_mid) 
            if cur_y > self.y_mid:
               scale_y = lerp(cur_y, 0,100, self.y_mid, self.y_max) 
            else:
                scale_y = lerp(cur_y, -100, 0, self.y_min, self.y_mid) 
            return int(scale_x), int(scale_y)
        return cur_x,cur_y
    
    def is_pressed(self):
        cur_x = self.x.read_analog()
        cur_y = self.y.read_analog()
        return cur_x > self.x_max or cur_y > self.y_max
        
        
js = Joystick(pin1, pin2)
js.calibrate_range()

while True:
    display.clear()
    if js.is_pressed():
        display.show(Image.HAPPY)
    else:

        x,y = js.read()
        s_x, s_y = int(x / 40), int(y / 40)
        display.set_pixel(2 + s_x, 2 + s_y, 9)
 
            