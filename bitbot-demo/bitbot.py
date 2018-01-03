from microbit import *
import neopixel

class BitBot:
    def __init__(self):
        self.np = neopixel.NeoPixel(pin13, 12)
        
    def _calc_speed(self, speed):
        return int(speed/100 * 1023)
    
    def left_motor_forward(self, speed=100):
        pin0.write_analog(self._calc_speed(speed))
        pin8.write_digital(False)
        
    def left_motor_reverse(self, speed=100):
        pin0.write_analog(self._calc_speed(100-speed))
        pin8.write_digital(True)

    
    def right_motor_forward(self, speed=100):
        pin1.write_analog(self._calc_speed(speed))
        pin12.write_digital(False)
        
    def right_motor_reverse(self, speed=100):
        pin1.write_analog(self._calc_speed(100-speed))
        pin12.write_digital(True)

    def left_motor_stop(self):
        pin0.write_digital(False)
        pin8.write_digital(False)

    def right_motor_stop(self):
        pin1.write_digital(False)
        pin12.write_digital(False)

    def stop(self):
        self.left_motor_stop()
        self.right_motor_stop()
        
    def forward(self, speed=100):
        self.left_motor_forward(speed)
        self.right_motor_forward(speed)
    
    def reverse(self, speed=100):
        self.left_motor_reverse(speed)
        self.right_motor_reverse(speed)
    
    def spin_left(self, speed=100):
        self.right_motor_forward(speed)
        self.left_motor_reverse(speed)
    
    def spin_right(self, speed=100):
        self.left_motor_forward(speed)
        self.right_motor_reverse(speed)
        
    def set_np(self, i, rgb):
        self.np[i] = rgb
        self.show_np()
    
    def set_np_all(self, rgb, count = None):
        if count == None:
            count = len(self.np)
        for i in range(count):
            self.np[i] = rgb
        self.show_np()
    
    def set_np_left(self, rgb, count=None):
        for i in range(len(self.np)//2):
            self.set_np(i, (0,0,0))
        if count == None:
            count = len(self.np)//2
        for i in range(count):
            self.np[i] = rgb
        self.show_np()
    
    def set_np_right(self, rgb, count=None):
        for i in range(len(self.np)//2):
            self.set_np(len(self.np)//2+ i, (0,0,0))
        if count == None:
            count = len(self.np)//2
        for i in range(count):
            self.np[i + len(self.np)//2] = rgb
        self.show_np()
    
    def clear_np(self):
        self.set_np_all((0,0,0))
        
    def show_np(self):
        self.np.show()
    
    def read_line_left(self):
        return pin11.read_digital()
        
    def read_line_right(self):
        return pin5.read_digital()
    
    def read_light_left(self):
        pin16.write_digital(False)
        return pin2.read_analog()
        
    def read_light_right(self):
        pin16.write_digital(True)
        return pin2.read_analog()
        
    def set_buzzer(self, state):
        pin14.write_digital(state)
