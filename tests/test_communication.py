import unittest
import serial
from unittest.mock import patch, MagicMock
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

class TestCommunication(unittest.TestCase):
    def setUp(self):
        with open('tests/test_config.json') as f:
            self.config = json.load(f)
            
    @patch('serial.Serial')
    def test_serial_connection(self, mock_serial):
        mock_serial.return_value = MagicMock()
        ser = serial.Serial(self.config['com_port'], 9600, timeout=1)
        self.assertTrue(mock_serial.called)
        
    @patch('serial.Serial')
    def test_command_sending(self, mock_serial):
        mock_serial.return_value = MagicMock()
        ser = serial.Serial(self.config['com_port'], 9600, timeout=1)
        command = b'rotate 1 1 100 cw\n'
        ser.write(command)
        mock_serial.return_value.write.assert_called_with(command)