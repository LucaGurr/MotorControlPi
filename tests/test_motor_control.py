import unittest
from unittest.mock import patch
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from tests.mock_hardware import MockMotorHAT

class TestMotorControl(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            self.config = json.load(f)
        self.hat1 = MockMotorHAT(self.config['hat_addresses'][0])
        self.hat2 = MockMotorHAT(self.config['hat_addresses'][1])

    def test_motor_initialization(self):
        self.assertIsNotNone(self.hat1)
        self.assertIsNotNone(self.hat2)
        
    def test_motor_movement(self):
        motor = self.hat1.get_stepper(200, 1)
        steps = 100
        for _ in range(steps):
            motor.onestep('forward', 'single')
        self.assertEqual(motor.current_position, steps)

    def test_motor_direction(self):
        motor = self.hat1.get_stepper(200, 1)
        motor.onestep('forward', 'single')
        self.assertEqual(motor.current_position, 1)
        motor.onestep('backward', 'single')
        self.assertEqual(motor.current_position, 0)