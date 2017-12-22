from dronekit import connect, VehicleMode, APIException, LocationGlobal
from pymavlink import mavutil
from time
from config import *
from helpers import *
import RPi.GPIO as GPIO
import sys
import argparse

###############################################################################
# Setup
###############################################################################
GPIO.setup(BURN_PIN, GPIO.OUT)
GPIO.output(BURN_PIN, GPIO.LOW)
start_time = time.time()

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
	sleep(1)

vehicle.armed = True
while not vehicle.armed:
	print 'Waiting for arm.'
	sleep(1)

print_status()
print '\n################# READY FOR FLIGHT #################\n'

###############################################################################
# Ascent
###############################################################################

prev_time_below_burn_alt = time()
while True:
	alt = vehicle.location.global_frame.alt
	if alt < BURN_ALTITUDE: 
		prev_time_below_burn_alt = time()
	else: 
		time_above = time() - prev_time_below_burn_alt
		print 'Above {}m for {} seconds'.format(BURN_ALTITUDE, time_above)
		if time_above > BURN_TIME_ABOVE:
			break

print_status()
print '\n################# REACHED BURN ALTITUDE #################\n'

###############################################################################
# Burn
###############################################################################

GPIO.output(BURN_PIN, GPIO.HIGH)
vehicle.mode = VehicleMode("GUIDED")

prev_time_above_burn_alt = time()
while True:
	alt = vehicle.location.global_frame.alt
	if alt > BURN_ALTITUDE: 
		prev_time_above_burn_alt = time()
	else: 
		time_below = time() - prev_time_above_burn_alt
		print 'Below {}m for {} seconds'.format(BURN_ALTITUDE, time_below)
		if time_below > BURN_TIME_ABOVE:
			break

GPIO.output(BURN_PIN, GPIO.LOW)

print_status()
print '\n################# VEHICLE DISCONNECTED #################\n'

###############################################################################
# Descent
###############################################################################

while True():
	print_status()
	time.sleep(1)

def print_status():
	print 'Time: {}\tMode: {}\t Alt: {}\tLoc: ({}, {})'.format(
		time(),
		vehicle.mode.name,
		vehicle.location.global_frame.alt,
		vehicle.location.global_frame.lat,
		vehicle.location.global_frame.lon)

def time():
	return time.time() - start_time

def exit(status):
	if vehicle is not None: vehicle.close()
	GPIO.cleanup()
	sys.exit(status)