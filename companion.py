from dronekit import connect, VehicleMode, APIException
from pymavlink import mavutil
from time import time
from config import *
from helpers import *
import sys
import argparse


###############################################################################
# Connect to pixhawk
###############################################################################
vehicle = None
try:
	vehicle = connect(PORT, baud=115200, wait_ready=True)
except Exception as e:
	print e
	print 'Failed to connect to pixhawk. exiting.'
	sys.exit(1)

###############################################################################
# Ascent
###############################################################################

prev_time_below_burn_alt = time()
while True:
	alt = vehicle.location.global_relate_frame.alt
	if alt < BURN_ALTITUDE: prev_time_below_burn_alt = time()
	else: 
		time_above = time() - prev_time_below_burn_alt
		print 'Above {}m for {} seconds'.format(BURN_ALTITUDE, time_above)
		if time_above > BURN_TIME_ABOVE:
			break

###############################################################################
# Burn
###############################################################################

###############################################################################
# Descent
###############################################################################
