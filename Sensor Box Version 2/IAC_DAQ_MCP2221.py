# Just in case the environment variables were not properly set
import os
os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"

import board
import busio
import time

import adafruit_vl53l0x
from cedargrove_nau7802 import NAU7802

# Load cell
loadCelSensor = NAU7802(board.I2C(), address=0x2a, active_channels=1)

# Time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tofSensor = adafruit_vl53l0x.VL53L0X(i2c)

force = 0
distance = 0

print("Starting measurements. \n")

with open('test3.dat', 'a') as test:
    test.write('load cell, distance, time\n')
    
with open('testReal.dat', 'a') as test:
    test.write('Load Cell (N), Distance, Time\n')

with open('testCal1.dat', 'a') as test:
    test.write('New calibration data\n')

# Perform measurements
try:
    while True:
        # Get sensor readings
        loadCellValue = loadCelSensor.read()
        tofValue = tofSensor.range

        # Output sensor data
        print("Load cell: {:.0f}, Distance: {:.0f}".format(loadCellValue, tofValue))

        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%H:%M:%S", named_tuple)

        a = -0.1137
        b = -686.68
        
        try:
            print(loadCellValue)
            gram = float(loadCellValue)*a + b
            print('Grams: ',gram)
            kilo = gram/1000
            force = kilo*9.81
            print('Force: ',force)
            distance = tofValue
            print('Distance: ',distance)
        except:
            pass


        with open('test3.dat', 'a') as test:
            test.write(f'{loadCellValue},{tofValue}, {time_string}\n')
            
        with open('testReal.dat', 'a') as test:
            test.write(f'{force}, {distance}, {time_string}\n')
            
        ValueCall = int(loadCellValue)
        with open('testCal2.dat', 'a') as test:
            test.write(f'{ValueCall}\n')
        
        # Sleep
        time.sleep(1)

# Exit
except KeyboardInterrupt:
    print("\nexiting...\n")
