import time
import json
from typing import Dict, Any

class MockMotorHAT:
    def __init__(self, address: int):
        self.address = address
        self.motors = {}
        for i in range(1, 5):
            self.motors[i] = MockStepper(i)

    def get_stepper(self, steps_per_rev: int, motor_id: int):
        return self.motors[motor_id]

class MockStepper:
    def __init__(self, motor_id: int):
        self.motor_id = motor_id
        self.current_position = 0
        self.is_running = False
        
    def onestep(self, direction, style):
        time.sleep(0.01)  # Simulate step delay
        step_value = 1 if direction == 'forward' else -1
        self.current_position += step_value
        return step_value