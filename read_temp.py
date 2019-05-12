import smbus
import time

# i2c channel to use and device address
channel = 1
address = 0x48

# memory registers for config and temperature
config_register = 0x01
temperature_register = 0x00

# 2's complement of a number
def twos_complement(values, bits):
    if (values & (1 << (bits - 1))) != 0:
        values = values - (1 << bits)
    return values

# Read temperature register and calculate degrees celsius
def get_temp():
    reading = temp_sensor_bus.read_i2c_block_data(address, temperature_register, 2)
    
    # shift first byte over 4 bits and remove last 4 bits of second bit
    reading_shifted = (reading[0] << 4) | (reading[1] >> 5)
    
    # after shift calculate 2s complement and convert registers values to degrees celsius
    return (twos_complement(reading_shifted, 12)) * 0.0625

def setup_temp():
    # Read configuration register
    values = temp_sensor_bus.read_i2c_block_data(address, config_register, 2)
    print('Previous configuration %s' % values)

    # Configure sampling
    values[1] = values[1] & 0b00111111
    values[1] = values[1] | (0b10 << 6)

    # Write sampling
    temp_sensor_bus.write_i2c_block_data(address, config_register, values)

    # Confirm config update
    values = temp_sensor_bus .read_i2c_block_data(address, config_register, 2)
    print('Updated configuration %s ' % values)

# Initialise the i2c bus
temp_sensor_bus = smbus.SMBus(channel)

setup_temp()

try:
    while 1:
        temperature = get_temp()
        
        print('%s degrees celsius' % round(temperature, 2))
        
        time.sleep(2)

except KeyboardInterrupt:
    print('Exiting.')
