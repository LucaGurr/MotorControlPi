import unittest
import sys
import os
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from tests.test_motor_control import TestMotorControl
from tests.test_communication import TestCommunication

def setup_logging():
    logging.basicConfig(
        filename='test_results/test_run.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

if __name__ == '__main__':
    os.makedirs('test_results', exist_ok=True)
    setup_logging()
    
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMotorControl)
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCommunication))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)