import unittest
import sys
from pathlib import Path
import logging

sys.path.append(str(Path(__file__).parent.parent))
from tests.test_motor_control import TestMotorControl, TestHardwareControl
from tests.test_communication import TestCommunication

def setup_logging():
    logging.basicConfig(
        filename='test_results/test_run.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

if __name__ == '__main__':
    import os
    os.makedirs('test_results', exist_ok=True)
    setup_logging()

    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMotorControl))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHardwareControl))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCommunication))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(not result.wasSuccessful())