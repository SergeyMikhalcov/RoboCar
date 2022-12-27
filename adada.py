from threading import Thread, Lock
from time import sleep, time


class Car:
    def __init__(self):
        self.value = 0
        self.lock = Lock()
        #self.next_move = 'stop'
        self.cur_rigth_wheel_state = 'stop'
        self.cur_left_wheel_state = 'stop'
        self.cur_rigth_wheel_velocity = 0
        self.cur_left_wheel_velocity = 0
        self.next_rigth_wheel_state = 'stop'
        self.next_left_wheel_state = 'stop'
        self.next_rigth_wheel_velocity = 0
        self.next_left_wheel_velocity = 0
        self.time_cycle = 0.5
        
        self.t = Thread(target = self.movement_cycle)
        self.t.daemon = True
        
    def movement_cycle(self):
        while True:
            sleep(0.00001)
            with self.lock:
                print(self)
                self.cur_rigth_wheel_state = self.next_rigth_wheel_state
                self.cur_left_wheel_state = self.next_left_wheel_state
                self.cur_rigth_wheel_velocity = self.next_rigth_wheel_velocity
                self.cur_left_wheel_velocity = self.next_left_wheel_velocity
                print(self)
                ##send to port values
                if (self.cur_rigth_wheel_velocity < self.cur_left_wheel_velocity):
                    sleep(self.cur_rigth_wheel_velocity*self.time_cycle)
                    self.cur_rigth_wheel_state = 'stop'
                    print(self)
                    sleep((self.cur_left_wheel_velocity - self.cur_rigth_wheel_velocity)*self.time_cycle)
                    self.cur_left_wheel_state = 'stop'
                    print(self)
                    sleep((1 - self.cur_left_wheel_velocity)*self.time_cycle)
                elif (self.cur_left_wheel_velocity < self.cur_rigth_wheel_velocity):
                    sleep(self.cur_left_wheel_velocity*self.time_cycle)
                    self.cur_left_wheel_state = 'stop'
                    print(self)
                    sleep((self.cur_rigth_wheel_velocity - self.cur_left_wheel_velocity)*self.time_cycle)
                    self.cur_rigth_wheel_state = 'stop'
                    print(self)
                    sleep((1 - self.cur_rigth_wheel_velocity)*self.time_cycle)
                else:
                    sleep(self.cur_rigth_wheel_velocity)
                    self.cur_rigth_wheel_state = 'stop'
                    self.cur_left_wheel_state = 'stop'
                    print(self)
                    sleep((1 - self.cur_rigth_wheel_velocity)*self.time_cycle)
                print(self)
                
    def set_next_move(self, rigth_wheel_state, left_wheel_state, rigth_wheel_velocity, left_wheel_velocity):
        self.lock.acquire()
        self.next_rigth_wheel_state = rigth_wheel_state
        self.next_left_wheel_state = left_wheel_state
        self.next_rigth_wheel_velocity = rigth_wheel_velocity
        self.next_left_wheel_velocity = left_wheel_velocity
        self.lock.release()
        
    def start_move(self):
        self.t.start()
        
    def __str__(self):
        return ("Car state is --\t"
               "Right wheel - {}, {}\t"
               "Left wheel - {}, {}\t"
               "Time - {}").format(self.cur_rigth_wheel_state, 
                                             self.cur_rigth_wheel_velocity,
                                             self.cur_left_wheel_state, 
                                             self.cur_left_wheel_velocity,
                                             time()) 

if __name__=="__main__":
    car = Car()
    car.start_move()
    sleep(2)
    car.set_next_move('forward', 'forward', 0.25, 0.5)
    sleep(4)
    car.set_next_move('forward', 'forward', 0.75, 0.25)
    sleep(5)
    