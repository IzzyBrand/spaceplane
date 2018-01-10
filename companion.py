from dronekit import connect, VehicleMode, APIException, LocationGlobal
from pymavlink import mavutil
import time
import numpy as np
from config import *
import RPi.GPIO as GPIO
import sys
import argparse

###############################################################################
# Functions
###############################################################################

start_time = time.time()
def mytime():
	return time.time() - start_time

def exit(status):
	if vehicle is not None: vehicle.close()
	GPIO.cleanup()
	sys.exit(status)

def print_status():
	print 'Time: {}\tMode: {}\t Alt: {}\tLoc: ({}, {})'.format(
		mytime(),
		vehicle.mode.name,
		vehicle.location.global_relative_frame.alt,
		vehicle.location.global_frame.lat,
		vehicle.location.global_frame.lon)

###############################################################################
# Setup
###############################################################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(BURN_PIN, GPIO.OUT)
GPIO.output(BURN_PIN, GPIO.LOW)
target_location = LocationGlobal(TARGET_LAT, TARGET_LON, 1000)

vehicle = None
try:
	vehicle = connect(PORT, baud=115200, wait_ready=True)
except Exception as e:
	print e
	print 'Failed to connect to pixhawk. exiting.'
	exit(1)

vehicle.mode = VehicleMode("MANUAL")

while not vehicle.mode.name == "MANUAL":
	print 'Waiting for MANUAL mode.'
	time.sleep(1)

vehicle.armed = True
while not vehicle.armed:
	print 'Waiting for arm.'
	time.sleep(1)

print_status()
print '\n################# READY FOR FLIGHT #################\n'

###############################################################################
# Ascent
###############################################################################

# maintain a circular buffer of altitude
alt_buffer_len 	= int(60/LOOP_DELAY)
alt_buffer 		= np.ones([alt_buffer_len]) * vehicle.location.global_relative_frame.alt
alt_buffer_ind 	= 0

prev_time_below_burn_alt = mytime()
while True:
	alt = vehicle.location.global_relative_frame.alt
	alt_buffer[alt_buffer_ind] = alt
	alt_buffer_ind += 1
	alt_buffer_ind = alt_buffer_ind % alt_buffer_len
	alt_diff = alt - alt_buffer[alt_buffer_ind]
	if (alt_diff < -50):
		print 'WARNING: descended {}m in 60 seconds. Disconnecting.'.format(alt_diff)
		break

	if alt < BURN_ALTITUDE: 
		prev_time_below_burn_alt = mytime()
	else: 
		time_above = mytime() - prev_time_below_burn_alt
		print 'Above {}m for {} seconds'.format(BURN_ALTITUDE, time_above)
		if time_above > BURN_TIME_ABOVE:
			break

	if alt_buffer_ind == 0: print_status()	# print status once every 60 seconds
	time.sleep(LOOP_DELAY)

print_status()
print '\n################# REACHED ALTITUDE: BURN STARTED #################\n'


###############################################################################
# Burn
###############################################################################

GPIO.output(BURN_PIN, GPIO.HIGH)
vehicle.mode = VehicleMode("GUIDED")
vehicle.simple_goto(target_location)

prev_time_above_burn_alt = mytime()
while True:
	alt = vehicle.location.global_relative_frame.alt
	if alt > BURN_ALTITUDE: 
		prev_time_above_burn_alt = mytime()
	else: 
		time_below = mytime() - prev_time_above_burn_alt
		print 'Below {}m for {} seconds'.format(BURN_ALTITUDE, time_below)
		if time_below > BURN_TIME_BELOW:
			break

	time.sleep(LOOP_DELAY)

GPIO.output(BURN_PIN, GPIO.LOW)

print_status()
print '\n################# VEHICLE DISCONNECTED: BURN STOPPED #################\n'

###############################################################################
# Descent
###############################################################################

while True:
	print_status()
	time.sleep(60)

