#!/usr/bin/env python3

# NOTE:
# using touch_device.grab() and ungrab() did not work using process calls to disable touch

import time
import argparse
from evdev import InputDevice
import subprocess
import psutil

DEBUG = False
TOUCHSCREEN_LOCK_DELAY = 2
# use `sudo evtest` to obtaintn the correct device path for your machine
STYLUS_DEVICE_PATH = '/dev/input/event4'  # Wacom sensor Pen
TOUCH_DEVICE_PATH = '/dev/input/event5'  # Wacom sensor Finger


stylus_device = InputDevice(STYLUS_DEVICE_PATH)  # Wacom sensor Pen
#touch_device = InputDevice(touch_device_path)  # Wacom sensor Finger


def disable_touch():
    if find_evtest_pid(TOUCH_DEVICE_PATH):
        print(f"Touch input already disabled.")
        return
  
    # Run evtest --grab to grab the input device
    command = ["evtest", "--grab", TOUCH_DEVICE_PATH]
    if DEBUG:
        print(f"Command: {''.join(command)}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.5)
    pid = process.pid

    if pid:
        print(f"Touch input has been disabled.")
        print(f"Evtest process ID: {pid}")  # Output the PID of the started process
    else:
        print("Failed to disable touch input.")


def enable_touch():
    # Find the process ID of the evtest command
    pid = find_evtest_pid(TOUCH_DEVICE_PATH)
    # Kill the process
    if pid:
        process = psutil.Process(pid)
        if DEBUG:
            print(f"Trying to kill process with ID {pid}")
        process.kill()
        print(f"Touch input has been enabled.")
    else:
        print("Could not find a evtest process to terminate.\nProbably the touchscreen is already active")


def find_evtest_pid(device_path):
    # Find the PID of the evtest process using the device path
    for proc in psutil.process_iter(["pid", "cmdline"]):
        cmdline = proc.info.get("cmdline")
        if cmdline and len(cmdline) > 2 and cmdline[0] == "evtest" and cmdline[2] == device_path:
            return proc.info["pid"]
    return None


def stylus_is_close(test = False):
    result = False
    if stylus_device.active_keys():
        result = True
   
    if test:
        print(f"Stylus is close: {result}")
    return result


def handle_stylus_proximity():
    if stylus_is_close():
        disable_touch()
    else:
        time.sleep(TOUCHSCREEN_LOCK_DELAY)
        if not stylus_is_close(): 
            enable_touch()

def parse_args():
    # Argument parser for enabling debug
    parser = argparse.ArgumentParser(description='Script for handling stylus proximity and touch input.')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--test-proximity', action='store_true', help='Test proximity')
    return parser.parse_args()

def main():
    global DEBUG
    args = parse_args()
    DEBUG = args.debug

    while True:
        if args.test_proximity:
            stylus_is_close(test=True)
        else:
            handle_stylus_proximity()


if __name__ == "__main__":
    main()
