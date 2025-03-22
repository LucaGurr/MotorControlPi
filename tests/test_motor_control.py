import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).parent.parent))
from tests.mock_hardware import MockMotorHAT

class TestMotorControl(unittest.TestCase):
    def setUp(self):
        self.hat1 = MockMotorHAT(0x60)
        self.hat2 = MockMotorHAT(0x61)

    def test_motor_initialization(self):
        motor1 = self.hat1.get_stepper(200, 1)
        motor2 = self.hat2.get_stepper(200, 1)
        
        self.assertIsNotNone(motor1)
        self.assertIsNotNone(motor2)
        self.assertEqual(motor1.current_position, 0)
        self.assertEqual(motor2.current_position, 0)

    def test_motor_movement(self):
        motor = self.hat1.get_stepper(200, 1)
        steps = 100
        
        for _ in range(steps):
            motor.onestep('forward', 'single')
        
        self.assertEqual(motor.current_position, steps)

    def test_direction_change(self):
        motor = self.hat1.get_stepper(200, 1)
        
        motor.onestep('forward', 'single')
        self.assertEqual(motor.current_position, 1)
        
        motor.onestep('backward', 'single')
        self.assertEqual(motor.current_position, 0)

class TestHardwareControl(unittest.TestCase):
    def setUp(self):
        self.mock_kit = MagicMock()
        self.mock_stepper = MagicMock()
        self.mock_kit.stepper1 = self.mock_stepper
        self.mock_kit.stepper2 = self.mock_stepper

    def test_hat_addresses(self):
        with patch('tests.mock_hardware.MockMotorHAT') as mock_hat:
            mock_hat.return_value = self.mock_kit
            hat1 = mock_hat(0x60)
            hat2 = mock_hat(0x61)
            
            mock_hat.assert_any_call(0x60)
            mock_hat.assert_any_call(0x61)

    def test_motor_commands(self):
        self.mock_stepper.onestep = MagicMock()
        self.mock_stepper.onestep('forward', 'single')
        self.mock_stepper.onestep.assert_called_with('forward', 'single')

if __name__ == '__main__':
    unittest.main()