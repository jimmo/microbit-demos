'Example heart rate monitor that prints heart rate to serial'
from microbit import *

HR_PIN = pin1

t = running_time()
    
while True:
    # Seeed ear clip HR monitor sends a high pulse every time a pulse is detected
    if HR_PIN.read_digital():
        t_new = running_time()
        print(str( 60000 / (t_new-t) ))
        
        t = t_new
        while HR_PIN.read_digital(): 
            pass
        
