from dronekit import connect, VehicleMode
import time
import numpy as np

vehicle = connect('/dev/ttyACM0', baud=115200, wait_ready=True)
vehicle.mode = VehicleMode('MANUAL')
vehicle.armed = True

while True:
    vehicle.channels.overrides['2'] = np.random.randint(1300,1700)
    vehicle.channels.overrides['1'] = np.random.randint(1300,1700)
    time.sleep(0.2)

