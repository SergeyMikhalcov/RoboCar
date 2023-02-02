from threading import Thread, Lock
from time import sleep, time
from PCF8574 import PCF8574
import numpy as np
from Wheel import Wheel
        
class CarWithTwoWheels:
    def __init__(self) -> None:
        self.array_for_port = np.zeros(8, dtype=np.bool8)
        self.right_wheel: Wheel = Wheel("Right Wheel", self.array_for_port[4: 6])
        self.left_wheel: Wheel = Wheel("Left Wheel", self.array_for_port[6: 8])
        self.control_thread = Thread(target=self.on_change)
        self.control_thread.daemon = True
        self._linear_velocity: float = (self.right_wheel.velocity + self.left_wheel.velocity) / 2
        self.wheel_base: float = 0.12
        self._angular_velocity: float = (self.left_wheel.velocity - self.right_wheel.velocity) / self.wheel_base
        self.is_control_running: bool = True
        
    def on_change(self):
        while self.is_control_running:
            sleep(0.05)
            #print(self.right_wheel)
            #print(self.left_wheel)
            print(self.array_for_port)
            # if self.ar_changes:
            #     self.send_to_port()    
            #     self.ar_changes = False
        
    def send_to_port(self):
        print(self.array_for_port)
    
    @property
    def linear_velocity(self) -> float:
        return self._linear_velocity
    
    @linear_velocity.setter
    def linear_velocity(self, value: float) -> None:
        self._linear_velocity = value
        self.left_wheel.velocity = value
        self.right_wheel.velocity = value
        
    @linear_velocity.deleter
    def linear_velocity(self) -> None:
        del self._linear_velocity
        
    @property
    def angular_velocity(self) -> float:
        return self._angular_velocity
    
    @angular_velocity.setter
    def angular_velocity(self, value: float) -> None:
        self._angular_velocity = value
        
    @angular_velocity.deleter
    def angular_velocity(self) -> None:
        del self._angular_velocity
        
    def start(self) -> None:
        self.control_thread.start()
        self.right_wheel.start()
        self.left_wheel.start()
        
    def stop(self) -> None:
        self.is_control_running = False
        self.right_wheel.stop()
        self.left_wheel.stop()
        
if __name__=="__main__":
    # wheel = WheelMotor("Check Motor", [False, False], 0.1)
    # wheel.start()
    # wheel.velocity = 0.1
    # sleep(2)
    # wheel.velocity = 0.5
    # sleep(2)
    # wheel.velocity = 1
    # sleep(2)
    # wheel.velocity = 0
    # sleep(2)
    # wheel.stop()
    # a = [False, False]
    # pwm = PWM(a, [False, False], [True, True], 2)
    # pwm.start()
    # i = 0
    # while i<10000:
    #     print(a)
    #     if i>5000:
    #         pwm.duty_cycle = 10
    #     i+=1
    # pwm.stop()
    # ac = ArrayClass()
    # ac.start()
    # sleep(4)
    CWTW = CarWithTwoWheels()
    CWTW.start()
    sleep(1)
    print("CHANGE")
    CWTW.linear_velocity = 1.0
    sleep(2)
    print("CHANGE")
    CWTW.linear_velocity = 0.2
    sleep(2)
    print("CHANGE")
    CWTW.linear_velocity = -0.1
    sleep(2)
    print("CHANGE")
    CWTW.linear_velocity = 0.5
    sleep(2)
    print("CHANGE")
    CWTW.linear_velocity = 1.0
    sleep(4)
    print("CHANGE")
    CWTW.stop()
    sleep(1)
    # car = Car()
    # car.start_move()
    # sleep(2)
    # car.set_next_move(Movement.FORWARD, Movement.FORWARD, 0.25, 0.5)
    # sleep(4)
    # car.set_next_move(Movement.FORWARD, Movement.FORWARD, 0.75, 0.25)
    # sleep(5)
    #check = CarCheckWheels()
    #check.start_move()