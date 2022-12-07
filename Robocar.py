#from pcf8574 import PCF8574
import time
import numpy as np
from pynput.keyboard import Key, Listener

class RoboCar:
    i2c_port_num = 1
    pcf_address = 0x25
    timestamp_for_move = 0.1 #in sec
    duty_cycle = 3 
    
    def __init__(self, port = i2c_port_num, address = pcf_address):
        #pcf = PCF8574(port, address)
        #self.port = pcf.port
        self.port = self.stop()
        
    def turn_right_wheel_back(self):
        return np.array([True, True, True, True, True, False, True, True], \
            dtype=bool)
        
    def turn_right_wheel_forward(self):
        return np.array([True, True, True, True, False, True, True, True], \
            dtype=bool)
    
    def turn_left_wheel_back(self):
        return np.array([True, True, True, True, True, True, True, False], \
            dtype=bool)
    
    def turn_left_wheel_forward(self):
        return np.array([True, True, True, True, True, True, False, True], \
            dtype=bool)
    
    def stop(self):
        return np.ones(8, dtype=bool)
    
    def move_forward(self):
        return np.bitwise_and(self.turn_right_wheel_forward(), 
                       self.turn_left_wheel_forward())
        
    def move_backward(self):
        return np.bitwise_and(self.turn_right_wheel_back(), 
                       self.turn_left_wheel_back())
        
    def turn_left(self):
        return self.turn_right_wheel_forward()
        
    def turn_right(self):
        return self.turn_left_wheel_forward()
        
    def spin_clockwise(self):
        return np.bitwise_and(self.turn_left_wheel_forward(), 
                       self.turn_right_wheel_back())
    
    def spin_counter_clockwise(self):
        return np.bitwise_and(self.turn_right_wheel_forward(), 
                       self.turn_left_wheel_back())
        
class RoboCarController:
    
    def __init__(self, robocar: RoboCar):
        self.robocar = robocar
    
    def on_press(self, key):
        print('{0} pressed'.format(key))
        if key==Key.left:
            self.robocar.turn_left()
        
        elif key==Key.right:
            self.robocar.turn_right()
        
        elif key==Key.up:
            self.robocar.move_forward()
        
        elif key==Key.down:
            self.robocar.move_backward()
        
        elif key==Key.ctrl_r:
            self.robocar.spin_clockwise()
        
        elif key==Key.shift_r:
            self.robocar.spin_counter_clockwise()
        
        #elif key==Key.esc:
        #    pass
        
        else:
            pass
        
    def on_release(self, key):
        print('{0} release'.format(key))
        self.robocar.stop()
        if key == Key.esc:
            return False
    
    
    def start_listen(self):
        # Collect events until released
        with Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            listener.join()
            
if __name__=="__main__":
    robocar = RoboCar()
    controller = RoboCarController(robocar)
    controller.start_listen()
    

    