#!bin/bash python3
from threading import Thread
from time import sleep

class PWM:
    def __init__(self, variable_for_modulation, max_v, min_v, signal_time, time_cycle=0.1):
        self.signal = variable_for_modulation
        self.max_v = max_v
        self.min_v = min_v
        self.signal_time = signal_time
        self.time_cycle = time_cycle
        self.t = Thread(target=self._run)
        self.t.daemon = True
        
    def _run(self):
        while self.is_running:
            sleep(0.000001)
            self.signal[:] = self.max_v
            sleep(abs(self.signal_time)*self.time_cycle)
            self.signal[:] = self.min_v
            sleep(self.time_cycle - abs(self.signal_time)*self.time_cycle)
            
    def start(self):
        self.is_running = True
        self.t.start()
        
    def stop(self):
        self.is_running = False