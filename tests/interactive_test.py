import sys
import time
from pathlib import Path
import json
import msvcrt
import argparse
import os

sys.path.append(str(Path(__file__).parent.parent))
from tests.mock_hardware import MockMotorHAT

class InteractiveTest:
    def __init__(self):
        self.hat1 = MockMotorHAT(0x60)
        self.hat2 = MockMotorHAT(0x61)
        self.current_hat = 1
        self.current_motor = 1
        self.step_size = 100
        self.direction = 'cw'

    def run(self):
        while True:
            os.system('cls')
            self.draw_interface()
            
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                self.handle_input(key)
            
            time.sleep(0.1)

    def draw_interface(self):
        print("Interactive Motor Test")
        print("\nCurrent Settings:")
        print(f"Current HAT: {self.current_hat}")
        print(f"Current Motor: {self.current_motor}")
        print(f"Step Size: {self.step_size}")
        print(f"Direction: {self.direction}")
        
        print("\nControls:")
        print("h - Switch HAT")
        print("m - Switch Motor")
        print("s - Change Step Size")
        print("d - Toggle Direction")
        print("SPACE - Move Motor")
        print("q - Quit")

    def handle_input(self, key):
        if key == 'h':
            self.current_hat = 2 if self.current_hat == 1 else 1
        elif key == 'm':
            self.current_motor = 2 if self.current_motor == 1 else 1
        elif key == 's':
            self.step_size = 200 if self.step_size == 100 else 100
        elif key == 'd':
            self.direction = 'ccw' if self.direction == 'cw' else 'cw'
        elif key == ' ':
            self.move_motor()
        elif key == 'q':
            sys.exit(0)

    def move_motor(self):
        hat = self.hat1 if self.current_hat == 1 else self.hat2
        motor = hat.get_stepper(200, self.current_motor)
        
        print(f"\nMoving motor {self.current_motor} on HAT {self.current_hat}...")
        for i in range(self.step_size):
            motor.onestep('forward' if self.direction == 'cw' else 'backward', 'single')
            time.sleep(0.01)
            if i % 10 == 0:
                print(f"Step {i+1}/{self.step_size}", end='\r')
        print("\nMovement complete!")
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description='Interactive Motor Test')
    parser.add_argument('--mock', action='store_true', help='Run in mock mode')
    args = parser.parse_args()

    if not args.mock:
        print("This script only runs in mock mode")
        sys.exit(1)

    test = InteractiveTest()
    test.run()

if __name__ == '__main__':
    main()