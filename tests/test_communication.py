import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).parent.parent))

class TestCommunication(unittest.TestCase):
    def setUp(self):
        self.serial_patcher = patch('serial.serialutil.SerialBase')
        self.mock_serial = self.serial_patcher.start()
        self.serial_instance = MagicMock()
        self.mock_serial.return_value = self.serial_instance

    def tearDown(self):
        self.serial_patcher.stop()

    def test_serial_connection(self):
        import serial
        ser = serial.Serial('COM3', 9600, timeout=1)
        self.mock_serial.assert_called_once()

    def test_command_sending(self):
        import serial
        ser = serial.Serial('COM3', 9600, timeout=1)
        command = b'rotate 1 1 100 cw\n'
        ser.write(command)
        self.serial_instance.write.assert_called_with(command)

    def test_response_reading(self):
        import serial
        ser = serial.Serial('COM3', 9600, timeout=1)
        expected_response = b'OK\n'
        self.serial_instance.readline.return_value = expected_response
        response = ser.readline()
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()