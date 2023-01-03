from threading import Thread, Lock
from time import sleep, time
from pcf8574 import PCF8574
import numpy as np
from enum import Enum

class Movement(Enum):
    UNDEFINED = 0
    FORWARD = 1
    BACKWARD = 2
    STOP = 3

class WheelMotor:
    time_cycle = 0.01
    
    def __init__(self, position, time_cycle = time_cycle):
        self.position = position
        self.velocity = 0
        self.state = Movement.STOP
        self.next_velocity = 0
        self.next_state = Movement.STOP
        self.time_cycle = time_cycle
        
        self.lock = Lock()
        self.t = Thread(target = self.movement_cycle)
        self.t.daemon = True
    
    def update_state(self):
        self.state = self.next_state
        self.velocity = self.next_velocity
    
    def set_next_state_velocity(self, state: Movement, velocity: float):
        self.lock.acquire()
        self.next_state = state
        self.next_velocity = velocity
        self.lock.release()
        
    def movement_cycle(self):
         while True:
            sleep(0.00001)
            with self.lock:
                print(self)
                self.update_state()
                print(self)
                sleep(self.velocity*self.time_cycle)
                self.state = Movement.STOP
                self.update_state()
                print(self)
                sleep((1 - self.velocity)*self.time_cycle)
                
    def __str__(self):
        return (
                "%s \t %s wheel: velocity: %f \t state: %s \t",
                "next_velocity: %f \t next_state: %s".format(
                    time(), self.position, self.velocity, self.state, 
                    self.next_velocity, self.next_state
                    )
                )
    
class CarCheckWheels:
    
    i2c_port_num = 1
    pcf_address = 0x25
    
    def __init__(self, port = i2c_port_num, address = pcf_address) -> None:        
        self.pcf = PCF8574(port, address)
        self.lock = Lock()
        self.time_cycle = 0.5
        self.move_array = np.ones(8, dtype=bool)
        
        self.right_wheel = WheelMotor()
        self.left_wheel = WheelMotor()
        
        #self.t = Thread(target = self.movement_cycle)
        #self.t.daemon = True
    
    def turn_right_wheel_back(self):
        self.move_array[4:6] = [True, False]
        
    def turn_right_wheel_forward(self):
        self.move_array[4:6] = [False, True]
        
    def stop_right_wheel(self):
        self.move_array[4:6] = [True, True]
    
    def turn_left_wheel_back(self):
        self.move_array[5:7] = [True, False]
    
    def turn_left_wheel_forward(self):
        self.move_array[5:7] = [False, True]
        
    def stop_left_wheel(self):
        self.move_array[5:7] = [True, True]
    
    def stop(self):
        self.pcf.port = np.ones(8, dtype=bool)
        
    def update_state(self):
        if self.right_wheel.state==Movement.FORWARD:
            self.turn_right_wheel_forward()
        elif self.right_wheel.state==Movement.BACKWARD:
            self.turn_right_wheel_back()
        elif self.right_wheel.state==Movement.STOP:
            self.stop_right_wheel()
        else:
            raise ValueError("Uncorrect movement on right wheel!!!")
        if self.left_wheel.state==Movement.FORWARD:
            self.turn_left_wheel_forward()
        elif self.left_wheel.state==Movement.BACKWARD:
            self.turn_left_wheel_back()
        elif self.left_wheel.state==Movement.STOP:
            self.stop_left_wheel()
        else:
            raise ValueError("Uncorrect movement on left wheel!!!")
        
        self.pcf.port = self.move_array
                
    def set_next_move(self, right_wheel_state, left_wheel_state, right_wheel_velocity, left_wheel_velocity):
        self.right_wheel.set_next_state_velocity(right_wheel_state, right_wheel_velocity)
        self.left_wheel.set_next_state_velocity(left_wheel_state, left_wheel_velocity)
        
    def start_move(self):
        sleep(2)
        self.right_wheel.set_next_state_velocity(Movement.FORWARD, 0.1)
        self.left_wheel.set_next_state_velocity(Movement.FORWARD, 0.7)
        sleep(2)
        self.right_wheel.set_next_state_velocity(Movement.FORWARD, 0.7)
        self.left_wheel.set_next_state_velocity(Movement.FORWARD, 0.1)
        sleep(2)
        self.right_wheel.set_next_state_velocity(Movement.BACKWARD, 0.7)
        self.left_wheel.set_next_state_velocity(Movement.FORWARD, 0.1)
        sleep(2)
        self.right_wheel.set_next_state_velocity(Movement.FORWARD, 0.1)
        self.left_wheel.set_next_state_velocity(Movement.BACKWARD, 0.7)
        sleep(2)
        self.right_wheel.set_next_state_velocity(Movement.BACKWARD, 0.7)
        self.left_wheel.set_next_state_velocity(Movement.BACKWARD, 0.7)
    # def __str__(self):
    #     return ("Car state is --\t"
    #            "Right wheel - {}, {}\t"
    #            "Left wheel - {}, {}\t"
    #            "Time - {}").format(self.cur_right_wheel_state, 
    #                                          self.cur_right_wheel_velocity,
    #                                          self.cur_left_wheel_state, 
    #                                          self.cur_left_wheel_velocity,
    #                                          time()) 

class Car:
    i2c_port_num = 1
    pcf_address = 0x25
    
    def __init__(self, port = i2c_port_num, address = pcf_address):        
        #self.pcf = PCF8574(port, address)
        self.lock = Lock()
        self.cur_right_wheel_state = Movement.STOP
        self.cur_left_wheel_state = Movement.STOP
        self.cur_right_wheel_velocity = 0
        self.cur_left_wheel_velocity = 0
        self.next_right_wheel_state = Movement.STOP
        self.next_left_wheel_state = Movement.STOP
        self.next_right_wheel_velocity = 0
        self.next_left_wheel_velocity = 0
        self.time_cycle = 0.5
        self.move_array = np.ones(8, dtype=bool)
        
        self.t = Thread(target = self.movement_cycle)
        self.t.daemon = True
    
    def turn_right_wheel_back(self):
        self.move_array[4:6] = [True, False]
        
    def turn_right_wheel_forward(self):
        self.move_array[4:6] = [False, True]
        
    def stop_right_wheel(self):
        self.move_array[4:6] = [True, True]
    
    def turn_left_wheel_back(self):
        self.move_array[5:7] = [True, False]
    
    def turn_left_wheel_forward(self):
        self.move_array[5:7] = [False, True]
        
    def stop_left_wheel(self):
        self.move_array[5:7] = [True, True]
    
    #def stop(self):
        #self.pcf.port = np.ones(8, dtype=bool)
        
    def update_state(self):
        if self.cur_right_wheel_state==Movement.FORWARD:
            self.turn_right_wheel_forward()
        elif self.cur_right_wheel_state==Movement.BACKWARD:
            self.turn_right_wheel_back()
        elif self.cur_right_wheel_state==Movement.STOP:
            self.stop_right_wheel()
        else:
            raise ValueError("Uncorrect movement on right wheel!!!")
        if self.cur_left_wheel_state==Movement.FORWARD:
            self.turn_left_wheel_forward()
        elif self.cur_left_wheel_state==Movement.BACKWARD:
            self.turn_left_wheel_back()
        elif self.cur_left_wheel_state==Movement.STOP:
            self.stop_left_wheel()
        else:
            raise ValueError("Uncorrect movement on left wheel!!!")
        
        self.pcf.port = self.move_array
    
    def movement_cycle(self):
        while True:
            sleep(0.00001)
            with self.lock:
                print(self)
                self.cur_right_wheel_state = self.next_right_wheel_state
                self.cur_left_wheel_state = self.next_left_wheel_state
                self.cur_right_wheel_velocity = self.next_right_wheel_velocity
                self.cur_left_wheel_velocity = self.next_left_wheel_velocity
                self.update()
                print(self)
                if (self.cur_right_wheel_velocity < self.cur_left_wheel_velocity):
                    sleep(self.cur_right_wheel_velocity*self.time_cycle)
                    self.cur_right_wheel_state = Movement.STOP
                    self.update()
                    print(self)
                    sleep((self.cur_left_wheel_velocity - self.cur_right_wheel_velocity)*self.time_cycle)
                    self.cur_left_wheel_state = Movement.STOP
                    self.update()
                    print(self)
                    sleep((1 - self.cur_left_wheel_velocity)*self.time_cycle)
                elif (self.cur_left_wheel_velocity < self.cur_right_wheel_velocity):
                    sleep(self.cur_left_wheel_velocity*self.time_cycle)
                    self.cur_left_wheel_state = Movement.STOP
                    self.update()
                    print(self)
                    sleep((self.cur_right_wheel_velocity - self.cur_left_wheel_velocity)*self.time_cycle)
                    self.cur_right_wheel_state = Movement.STOP
                    self.update()
                    print(self)
                    sleep((1 - self.cur_right_wheel_velocity)*self.time_cycle)
                else:
                    sleep(self.cur_right_wheel_velocity)
                    self.cur_right_wheel_state = Movement.STOP
                    self.cur_left_wheel_state = Movement.STOP
                    self.update()
                    print(self)
                    sleep((1 - self.cur_right_wheel_velocity)*self.time_cycle)
                print(self)
                
    def set_next_move(self, right_wheel_state, left_wheel_state, right_wheel_velocity, left_wheel_velocity):
        self.lock.acquire()
        self.next_right_wheel_state = right_wheel_state
        self.next_left_wheel_state = left_wheel_state
        self.next_right_wheel_velocity = right_wheel_velocity
        self.next_left_wheel_velocity = left_wheel_velocity
        self.lock.release()
        
    def start_move(self):
        self.t.start()
        
    def __str__(self):
        return ("Car state is --\t"
               "Right wheel - {}, {}\t"
               "Left wheel - {}, {}\t"
               "Time - {}").format(self.cur_right_wheel_state, 
                                             self.cur_right_wheel_velocity,
                                             self.cur_left_wheel_state, 
                                             self.cur_left_wheel_velocity,
                                             time()) 

if __name__=="__main__":
    # car = Car()
    # car.start_move()
    # sleep(2)
    # car.set_next_move(Movement.FORWARD, Movement.FORWARD, 0.25, 0.5)
    # sleep(4)
    # car.set_next_move(Movement.FORWARD, Movement.FORWARD, 0.75, 0.25)
    # sleep(5)
    check = CarCheckWheels()
    check.start_move()