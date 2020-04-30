# CamJam EduKit 2 - Sensors (GPIO Zero)
# Worksheet 5 - Movement

# Import Python header files
from gpiozero import MotionSensor
from datetime import datetime
import time
import os

datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
print("Starting PIR.py")


os.system( "curl 192.168.0.10/switch_cammode.cgi?mode=shutter")
# Set a variable to hold the GPIO Pin identity
pir = MotionSensor(17)

print("Waiting for PIR to settle")
pir.wait_for_no_motion()

print("PIR Module Test (CTRL-C to exit)")

# Variables to hold the current and last states
currentstate = False
previousstate = False

try:
    # Loop until users quits with CTRL-C
    while True:
        # Read PIR state
        currentstate = pir.motion_detected

        # If the PIR is triggered
        if currentstate == True and previousstate == False:
            print("    Motion detected!")
            # cmd = "git --version"
            # returned_value = os.system(cmd)  # returns the exit code in unix
            # print('returned value:', returned_value)

            camera_command = "curl 192.168.0.10/exec_shutter.cgi?com=1st2ndpush && sleep 3 && curl 192.168.0.10/exec_shutter.cgi?com=2nd1strelease"
            os.system(camera_command)

            # Record previous state
            previousstate = True
        # If the PIR has returned to ready state
        elif currentstate == False and previousstate == True:
            print("    No Motion")
            previousstate = False

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print("    Quit")
