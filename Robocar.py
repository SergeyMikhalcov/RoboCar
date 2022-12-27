from pcf8574 import PCF8574
from enum import Enum
import time
import numpy as np
from pynput.keyboard import Key, Listener
import cv2
from threading import Thread

class Movement(Enum):
    UNDEFINED = 0
    FORWARD = 1
    RIGHT = 2 
    LEFT = 3
    STOP = 4
    SPIN_CLOCKWISE = 5
    SPIN_COUNTERCLOCKWISE = 6    
   
class RoboThread:
    self.stopped = True
    self.t = Thread(target = self.update, args=())
    self.t.daemon = True   
    
    def start(self):
        self.stopped = False
        self.t.start()
        
    def stop(stop):
        self.stopped = True
        
    def update(self, duty_cycle, func):
        while True:
            if self.stopped is True:
                break
            
                
                
    
class RoboCar:
    i2c_port_num = 1
    pcf_address = 0x25
    timestamp_for_move = 0.1 #in sec
    duty_cycle = 3 
    
    def __init__(self, port = i2c_port_num, address = pcf_address):
        self.pcf = PCF8574(port, address)
        self.stop()
        #self.port = pcf.port
        #self.port = self.stop()
        
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
        self.pcf.port = np.ones(8, dtype=bool)
    
    def move_forward(self):
        self.pcf.port = np.bitwise_and(self.turn_right_wheel_forward(), 
                       self.turn_left_wheel_forward())
        
    def move_backward(self):
        self.pcf.port = np.bitwise_and(self.turn_right_wheel_back(), 
                       self.turn_left_wheel_back())
        
    def turn_left(self):
        self.pcf.port = self.turn_right_wheel_forward()
        
    def turn_right(self):
        self.pcf.port = self.turn_left_wheel_forward()
        
    def spin_clockwise(self):
        self.pcf.port = np.bitwise_and(self.turn_left_wheel_forward(), 
                       self.turn_right_wheel_back())
    
    def spin_counter_clockwise(self):
        self.pcf.port = np.bitwise_and(self.turn_right_wheel_forward(), 
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
            
    def find_next_movement(img_init, min_color=np.array([13, 40, 0]), max_color=np.array([70, 255, 255])):
        img = cv2.cvtColor(img_init, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img[img.shape[0]//2-1:], min_color, max_color)
        cv2.imshow("Mask", mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            c = max(contours, key = cv2.contourArea)
            epsilon = 0.02*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)
            arg_sorted = np.argsort(approx, axis=0)
            y_sorted = arg_sorted[:, :, 1].flatten()
            #print(y_sorted, approx)
            x_cur_top = int(np.mean(approx[y_sorted][:2][:, :, 0]))
            x_cur_bot = int(np.mean(approx[y_sorted][2:][:, :, 0]))
            #print(x_cur_top, x_cur_bot)
            y_cur_top = int(np.mean(approx[y_sorted][:2][:, :, 1]))
            y_cur_bot = int(np.mean(approx[y_sorted][2:][:, :, 1]))
            x_center = mask.shape[1] // 2
            print(x_cur_top - x_center, " ", x_cur_bot - x_center)
            if (abs(x_cur_top - x_center)<20) and (abs(x_cur_bot - x_center)<20):
                print("FORWARD")
            elif (x_cur_top > x_center) and (x_cur_bot < x_center): 
                print("LEFT")
            elif (x_cur_top > x_center) and (x_cur_bot > x_center): 
                print("LEFT")
            elif (x_cur_top < x_center) and (x_cur_bot > x_center):
                print("RIGHT")
            elif (x_cur_top < x_center) and (x_cur_bot < x_center):
                print("RIGHT")
            res = cv2.drawContours(img_init[img.shape[0]//2-1:], approx, -1, (0, 255, 0), 3)
            cv2.line(img_init[img.shape[0]//2-1:], (x_center, y_cur_top), (x_center, y_cur_bot), (0, 0, 255), 3)
            cv2.line(img_init[img.shape[0]//2-1:], (x_cur_top, y_cur_top), (x_cur_bot, y_cur_bot), (255, 0, 0), 3)
            cv2.imshow("Frame", res)
        cv2.waitKey()
        return 
            
if __name__=="__main__":
    robocar = RoboCar()
    controller = RoboCarController(robocar)
    controller.start_listen()
    

    