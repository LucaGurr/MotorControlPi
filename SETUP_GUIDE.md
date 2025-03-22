# Stepper Motor Control System Setup Guide

## Prerequisites

- Windows 10/11 computer
- Raspberry Pi Zero
- USB cable (for Pi-to-Computer connection)
- 2× Adafruit DC & Stepper Motor HAT
- 4× Stepper Motors
- 12V Power supply for motors

## 1. Raspberry Pi Initial Setup

### Operating System Installation
1. Download "Raspberry Pi Imager" from the official Raspberry Pi website
2. Install and launch Raspberry Pi Imager
3. Choose "Raspberry Pi OS Lite" as the operating system
4. Select your SD card
5. Click "Write" and wait for completion

### Enable USB Gadget Mode
1. After writing the OS, open the boot partition of the SD card
2. Edit `config.txt` and add this line at the end:
   ```
   dtoverlay=dwc2,g_serial
   ```
3. Edit `cmdline.txt` and add after `rootwait`:
   ```
   modules-load=dwc2,g_serial
   ```

## 2. Hardware Setup

### HAT Assembly
1. Stack the first HAT onto the Raspberry Pi
   - Keep default address (0x60) - no jumper needed
2. Stack the second HAT on top
   - Set address jumper to 0x61
3. Connect stepper motors:
   - HAT 1: Motors 1-2
   - HAT 2: Motors 3-4
4. Connect 12V power supply to both HATs

### USB Connection
1. Connect Raspberry Pi to computer via USB cable
2. Wait for Windows to detect new hardware

## 3. Windows Setup

### Driver Installation
1. Open Device Manager
2. Find "USB Serial Device" or "Unknown Device"
3. Right-click → Update Driver
4. Choose "Browse my computer"
5. Select "Let me pick from a list"
6. Choose "USB Serial Device"
7. Note the assigned COM port number (you'll need this later)

### Software Installation
1. Install Python 3.8 or higher from python.org
2. Open Command Prompt as Administrator
3. Install required package:
   ```bash
   pip install pyserial
   ```

## 4. Raspberry Pi Configuration

### First Boot
1. Connect to Raspberry Pi via SSH:
   ```bash
   ssh pi@raspberrypi.local
   ```
   Default credentials:
   - Username: `pi`
   - Password: `raspberry`

### Enable I2C
1. Run configuration utility:
   ```bash
   sudo raspi-config
   ```
2. Navigate to: Interface Options → I2C → Enable
3. Reboot the Pi:
   ```bash
   sudo reboot
   ```

### Install Required Software
1. Update package list:
   ```bash
   sudo apt update
   ```
2. Install Python and I2C tools:
   ```bash
   sudo apt install -y python3-pip i2c-tools
   ```
3. Install required Python package:
   ```bash
   sudo pip3 install adafruit-circuitpython-motorkit
   ```

### Setup Motor Control Software
1. Copy the motor control script to the Pi:
   ```bash
   scp pi_code.py pi@raspberrypi.local:~/
   ```
2. Make the script executable:
   ```bash
   chmod +x pi_code.py
   ```
3. Run the script:
   ```bash
   python3 pi_code.py
   ```

## 5. Testing the System

1. On your Windows computer, run:
   ```bash
   python motor_control.py
   ```
2. Test basic movement:
   ```
   rotate 1 1 100 cw
   ```
   This rotates motor 1 on HAT 1 clockwise for 100 steps

## Troubleshooting

### Cannot Find COM Port
- Check Device Manager
- Try different USB ports
- Reinstall USB Serial driver
- Verify USB cable is data-capable (not charge-only)

### Connection Timeout
- Verify Pi is powered on
- Check USB cable connection
- Restart Pi and computer
- Confirm Pi script is running

### Motors Not Moving
- Check 12V power supply connection
- Verify motor wiring
- Test I2C connection:
  ```bash
  sudo i2cdetect -y 1
  ```
  Should show addresses 60 and 61

### Common Error Messages
- "Port not found": Double-check COM port number in Windows Device Manager
- "Connection refused": Verify Pi script is running
- "I2C Error": Check HAT connections and addresses
- "Permission denied": Run with sudo on Pi or admin privileges on Windows

## Additional Tips

1. Always power cycle in this order:
   - Power off 12V supply
   - Shut down Pi
   - Disconnect USB
   - Reconnect in reverse order

2. For reliability:
   - Keep USB and motor cables separated
   - Use a good quality 12V power supply
   - Ensure proper cooling for the motor HATs

3. Regular Maintenance:
   - Check motor connections monthly
   - Verify HAT mounting screws are tight
   - Update software as needed