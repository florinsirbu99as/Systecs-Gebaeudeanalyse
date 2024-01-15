

# Import the smbus module for I2C communication
import smbus 

# Define constants for the I2C address, bus number, and register addresses
GE_I2C_ADDRESS = 0X69
RPI_BUS = 0X01

GE_POWER_CTL_REG = 0x00 
GE_RESET_REG = 0x01 
GE_FPSC_REG = 0x02 
GE_INT_CTL_REG = 0x03 
GE_STAT_REG = 0x04 
GE_SCLR_REG = 0x05 


# Define constants for various configuration values
GE_PCTL_NORMAL_MODE = 0x00 
GE_PCTL_SLEEEP_MODE = 0x10 
GE_PCTL_STAND_BY_60S_MODE = 0x20


# Define constants for specific bit patterns
GE_RST_FLAG_RST = 0x30
GE_RST_INITIAL_RST = 0x3F

GE_FPSC_1FPS = 0x01
GE_FPSC_10FPS = 0x00

GE_INTC_ABS = 0b00000001
GE_INTC_DIF = 0b00000011
GE_INTC_OFF = 0b00000000

GE_SCLR_CLR = 0b00000110

# Function to create an I2C device
def get_i2c_device(address, busnum, i2c_interface=None, **kwargs):
    return i2c_driver(address, busnum, i2c_interface, **kwargs)

# Class representing an I2C driver
class i2c_driver(object):
    def __init__(self, address, busnum, i2c_interface=None):
        self._address = address
        self._bus = smbus.SMBus(busnum)

    def write8(self, register, value):                                                  # Write a byte of data to a specified register
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value)

    def read16(self, register, little_endian=True):                                     # Read a 16-bit word of data from a specified register
        result = self._bus.read_word_data(self._address, register) & 0xFFFF
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result


# Class representing the AMG8833 sensor
class AMG8833(object):
    def __init__(self, addr=GE_I2C_ADDRESS, bus_num=RPI_BUS):
        self.device = get_i2c_device(addr, bus_num)
        self.set_sensor_mode(GE_PCTL_NORMAL_MODE)                                    # Initialize the sensor with specific configuration settings
        self.reset_flags(GE_RST_INITIAL_RST) 
        self.set_interrupt_mode(GE_INTC_OFF) 
        self.set_sample_rate(GE_FPSC_10FPS) 


    def set_sensor_mode(self, mode):
        self.device.write8(GE_POWER_CTL_REG, mode)                                  # Set the sensor mode (normal mode, sleep mode, etc.)
        

    def reset_flags(self, value):
        self.device.write8(GE_RESET_REG, value)                                     # Reset specific flags or the entire sensor
        

    def set_sample_rate(self, value):
        self.device.write8(GE_FPSC_REG, value)                                      # Set the sample rate of the sensor
        

    def set_interrupt_mode(self, mode):
        self.device.write8(GE_INT_CTL_REG, mode)                                    # Set the interrupt mode (absolute, differential, or off)
        

    def clear_status(self, value):
        self.device.write8(GE_SCLR_REG, value)                                      # Clear specific status bits
        

    def read_temp(self, PIXEL_NUM):                                                 # Read temperature values from the sensor's pixel array
        T_arr = [] 
        status = False 
        for i in range(0, PIXEL_NUM):
            raw = self.device.read16(GE_PIXEL_BASE + (i << 1))		
            converted = self.twos_compl(raw) * 0.25
            if converted < -20 or converted > 100:
                return True, T_arr 
            T_arr.append(converted)
        return status, T_arr
    

    def read_thermistor(self):                                                  # Read temperature from the thermistor
        raw = self.device.read16(GE_TTHL_REG) 
        return self.signed_conv(raw) * 0.0625 
    

    def twos_compl(self, val):                                                  # Convert a 12-bit two's complement value to a signed float
        if 0x7FF & val == val:
            return float(val)
        else:
            return float(val - 4096)
        
        
    def signed_conv(self, val):                                                 # Convert a signed 11-bit value to a signed float
        if 0x7FF & val == val:
            return float(val)
        else:
            return -float(0x7FF & val)

