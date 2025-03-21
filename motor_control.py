import serial
import sys
import time
import subprocess
import os

def install_dependencies():
    print("Checking and installing dependencies...")
    try:
        import pip
    except ImportError:
        print("Installing pip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"])
    print("Dependencies installed successfully!")

class MotorController:
    def __init__(self):
        # Detect OS and set appropriate port
        if sys.platform.startswith('win'):
            self.port = None  # Will be detected automatically
            self.available_ports = self.get_available_ports()
        else:
            self.port = '/dev/ttyACM0'
        
        self.baudrate = 9600
        self.serial = None
        self.max_retries = 5
        self.retry_delay = 5  # seconds

    def get_available_ports(self):
        """Get list of available COM ports"""
        ports = []
        for i in range(256):
            try:
                port = f'COM{i}'
                s = serial.Serial(port)
                s.close()
                ports.append(port)
            except (OSError, serial.SerialException):
                pass
        return ports

    def auto_detect_port(self):
        """Automatically detect the correct COM port"""
        for port in self.available_ports:
            try:
                test_serial = serial.Serial(port, self.baudrate, timeout=1)
                test_serial.write(b"TEST\n")
                response = test_serial.readline().decode().strip()
                if response == "OK":
                    test_serial.close()
                    return port
                test_serial.close()
            except:
                continue
        return None

    def connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                if self.serial:
                    self.serial.close()
                
                # Auto-detect port on Windows
                if sys.platform.startswith('win') and not self.port:
                    self.port = self.auto_detect_port()
                    if not self.port:
                        raise serial.SerialException("Could not auto-detect Raspberry Pi port")

                self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
                print(f"Connected to {self.port}")
                return True
            except serial.SerialException as e:
                retries += 1
                if retries < self.max_retries:
                    print(f"Connection attempt {retries} failed. Retrying in {self.retry_delay} seconds...")
                    print(f"Error: {str(e)}")
                    time.sleep(self.retry_delay)
                else:
                    print(f"Failed to connect after {self.max_retries} attempts: {e}")
                    return False

    def send_command(self, command):
        if not self.serial or not self.serial.is_open:
            if not self.connect():
                return "Not connected"
        
        try:
            self.serial.write(f"{command}\n".encode())
            response = self.serial.readline().decode().strip()
            return response
        except serial.SerialException as e:
            print(f"Connection lost: {e}")
            self.serial = None
            return "Connection lost"

    def rotate_motor(self, hat_id, motor_id, steps, direction):
        command = f"ROTATE,{hat_id},{motor_id},{steps},{direction}"
        return self.send_command(command)

    def close(self):
        if self.serial:
            self.serial.close()

def main():
    # Install dependencies first
    install_dependencies()
    
    controller = MotorController()
    
    if not controller.connect():
        print("Initial connection failed. Will retry on commands.")

    print("\nStepper Motor Control")
    print("-------------------")
    print("Commands:")
    print("rotate <hat_id> <motor_id> <steps> <direction>")
    print("  hat_id: 1 or 2")
    print("  motor_id: 1 or 2")
    print("  steps: number of steps")
    print("  direction: cw (clockwise) or ccw (counter-clockwise)")
    print("quit - Exit program")

    try:
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                break
                
            parts = command.split()
            if len(parts) == 0:
                continue

            if parts[0] == 'rotate' and len(parts) == 5:
                hat_id = int(parts[1])
                motor_id = int(parts[2])
                steps = int(parts[3])
                direction = parts[4]

                if hat_id not in [1, 2] or motor_id not in [1, 2]:
                    print("Invalid hat_id or motor_id. Must be 1 or 2.")
                    continue

                if direction not in ['cw', 'ccw']:
                    print("Invalid direction. Must be 'cw' or 'ccw'.")
                    continue

                response = controller.rotate_motor(hat_id, motor_id, steps, direction)
                print(f"Response: {response}")
            else:
                print("Invalid command. Use 'rotate <hat_id> <motor_id> <steps> <direction>' or 'quit'")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        controller.close()

if __name__ == "__main__":
    main()