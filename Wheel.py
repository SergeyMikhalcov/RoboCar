#! bin/bash python3
from threading import Thread
import PWM
from enum import Enum
from typing import List
        
class Movement(Enum):
    UNDEFINED = 0
    FORWARD = 1
    BACKWARD = 2
    STOP = 3

class Wheel:
    time_cycle = 0.05
    
    def __init__(self, description: str, ar_for_ports: List[bool], time_cycle = time_cycle):
        self.description: str = description
        self.is_running: bool = False
        self._velocity: float = 0.0
        self._state: Movement = Movement.STOP
        self.time_cycle = time_cycle
        self.PWM = PWM(ar_for_ports, [False, False], [False, False], 1, time_cycle)
        
    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, value: float) -> None:
        self._velocity = value
        self.PWM.signal_time = value
        if value < 0:
            self.state = Movement.BACKWARD
            self.PWM.max_v[:] = [True, False]
        elif value > 0:
            self.state = Movement.FORWARD
            self.PWM.max_v[:] = [False, True]
        else:
            self.state = Movement.STOP
            self.PWM.max_v[:] = [False, False]

    @velocity.deleter
    def velocity(self) -> None:
        del self._velocity
    
    @property
    def state(self) -> Movement:
        return self._state

    @state.setter
    def state(self, value) -> None:
        self._state = value
        
    @state.deleter
    def state(self) -> None:
        del self._state
    
    def start(self) -> None:
        self.is_running = True
        self.PWM.start()
        
    def stop(self) -> None:
        self.is_running = False
        self.PWM.is_running = False
                
    def __str__(self) -> str:
        return ("{x.description} velocity: {x.velocity} \t state: {x.state.name}".format( x=self )
                )