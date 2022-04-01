import board
import busio
import smbus
import time
import adafruit_tsl2591

from adafruit_extended_bus import ExtendedI2C as I2C

# code for using ldr sensor with i2c buses
# also downloaded adafruit_tsl2591 from source to get library
# in order to use must update boot/config.txt file to include bus using the following:
# dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=14,i2c_gpio_scl=4


# initalize ldr in default gpio
i2c = board.I2C()
sensor = adafruit_tsl2591.TSL2591(i2c)

print('sensor 1', sensor.visible)

# initalize ldr in bus 5 (online seems to indicate starting with the highest bus and work through lowest bus in config.txt)
second_sensor = I2C(5)
sensor_two = adafruit_tsl2591.TSL2591(second_sensor)
print('sensor 2', sensor_two.visible)

# third_sensor = busio.I2C(15, 18)
# fourth_sensor = busio.I2C(20, 21)

# get i2c bus
bus5 = smbus.SMBus(5)
# bus3 = smbus.SMBus(3)
# bus4 = smbus.SMBus(4)

delay = 0.05

# while True:
    # reading = bus5.read_i2c_block_data(0x29, 24)
    # print('reading ---', reading)
