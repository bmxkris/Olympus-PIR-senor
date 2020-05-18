# CamJam EduKit 2 - Sensors (GPIO Zero)
# Worksheet 5 - Movement

# Import Python header files
from gpiozero import MotionSensor
from datetime import datetime
import time
import os
import subprocess

camera_SSID = ""
wifi_sleep_time = 10
camera_interval_time = 5

print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " Starting PIR.py")

# do we have the network available?
print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " Checking camera is available")

try:
    while subprocess.check_output(['sudo', 'iwgetid']).split('"')[1] != camera_SSID:
        print (datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " WiFi network not found: " + subprocess.check_output(['sudo', 'iwgetid']).split('"')[1])
        # Wait for 5 seconds
        time.sleep(wifi_sleep_time)

except Exception, e:
    print e

print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " Camera found, sending set up command")
os.system( "curl 192.168.0.10/switch_cammode.cgi?mode=shutter")
# Set a variable to hold the GPIO Pin identity
pir = MotionSensor(17)

print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " Waiting for PIR to settle")
pir.wait_for_no_motion()

print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + " Olympus PIR Module (CTRL-C to exit)")

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
            
            print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + "    Motion detected!")

            print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + "    Push!")
            os.system( "curl 192.168.0.10/exec_shutter.cgi?com=1st2ndpush")

            time.sleep(camera_interval_time)

            print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + "    Release!")
            os.system("curl 192.168.0.10/exec_shutter.cgi?com=2nd1strelease")

            # Record previous state
            previousstate = True
        # If the PIR has returned to ready state
        elif currentstate == False and previousstate == True:
            print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + "    No Motion")
            previousstate = False

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print( datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)") + "    Quit")
