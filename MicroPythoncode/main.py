///\author Twan Wieggers
import time
import pycom
import machine
from network import LoRa
import socket
import time
import ubinascii
import struct
import ustruct
import math
from unit_testing import *

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('D85E148856D86DB45DB888CAB77B96FC')
dev_eui = ubinascii.unhexlify('70B3D57ED00581D2')
max_humdity = 255
send_delay = 300
temp_offset = -7
humd_offset = 3.2

dht = SI7006A20()
li = LTR329ALS01()
alt = MPL3115A2(mode=PRESSURE)
pycom.heartbeat(False)

## this is the function for making the connection to the things network application.
#
# @brief it uses the dev_eui, app_eui and the app_key from the application on the things network
# it keeps trying to connect to the network
def lora_connection():
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
    while not lora.has_joined():
        # set_led_red()
        time.sleep(2.5)
        print('Not yet joined...')

    # set_led_green()
    print('Joined')
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(True)
    return(s)

##
# @brief This function uses the already made objects from the library and calls their functions to receive the right data
#
# @return The function returns a tuple of (pressure, temperature, light, humidity)
def receive_sensor_value():
    """
    Retrieve sensor values for pressure, temperature, light, and humidity

    Returns:
    Tuple of floats: (pressure, temperature, light, humidity)
    """
    pressure = alt.pressure()
    temp = dht.temperature()
    light = li.lux()
    humdity = dht.humidity()
    return (pressure,temp,light,humdity)

## the function recieves the raw pressure and do it times 0.01 to get the value in mBar.
# @param pressure the raw pressure value
# for sending the data over lora we can use max of 255 to fit it in 1 bytes sow we do -900
# in the decoder we add the 900 back to it.
def calculate_pressure(pressure):
    pres = pressure*0.01 -900
    pres = int(pres)
    return(pres)

def calculate_temp(temp):
    """
    Scales the temperature value and offsets it by a specified amount. It also handles negative temperatures.
    Handles negative temperature by setting a bit to 1 if it is negative.
    :param temp: The raw temperature value
    :return: (fulltemp, decimaltemp, minus)
    """
    if(temp < 0):
        minus = 1
        temp = temp * (-1)
        fulltemp = int(temp)
        decimaltemp = int((temp - fulltemp)*10)
    else:
        fulltemp = int(temp) + temp_offset
        decimaltemp = int((temp - fulltemp)*10)
        minus = 0
    fulltemp = fulltemp + temp_offset
    return(fulltemp,decimaltemp,minus)

def calculate_light(light):
    """
    Scales the light value to fit in 1 byte. It uses a logarithmic scale because lux is a logarithmic value
    @param light: the raw light value
    @return: the scaled light value
    """
    lightvalue = int(light)
    if(lightvalue < 123):
        lightvalue = lightvalue
    else:
        lightvalue = int(round(math.log(light,1.04),0))
        if(lightvalue > 255):
            lightvalue = 255
    return(lightvalue)

def calculate_humd(humdity):
    """
    Scales the humidity value to fit in 1 byte and offsets it by a specified amount.

    @param humdity: The raw humidity value from the sensor
    @type humdity: float

    @return: The scaled and offset humidity value
    @rtype: int
    """
    humdity = humdity * humd_offset
    humdity = int(humdity)
    return(humdity)

def construct_payload(fulltemp,decimaltemp,pressure,humdity,light,minus):
    """
    Creates a payload of sensor data to be sent over the LoRa network.

    @param fulltemp: the full temperature value, scaled and offset
    @type fulltemp: int
    @param decimaltemp: the decimal part of the temperature value
    @type decimaltemp: int
    @param pressure: the pressure value, scaled and offset
    @type pressure: int
    @param humdity: the humidity value, scaled and offset
    @type humdity: int
    @param light: the light value, scaled and offset
    @type light: int
    @param minus: a flag indicating if the temperature is negative
    @type minus: int
    @return: the payload to be sent over the LoRa network
    @rtype: bytes
    """
    fulltempstruct = ustruct.pack('b',fulltemp)
    decitempstruct = ustruct.pack('b',decimaltemp)
    presstruct = ustruct.pack('b',pressure)
    humditystruct = ustruct.pack('b',humdity)
    lightstruct = ustruct.pack('b',light)
    minusstruct = ustruct.pack('b',minus)
    payload = presstruct + fulltempstruct + decitempstruct + lightstruct + humditystruct + minusstruct
    return(payload)


    ##
    # set the led to red
    def set_led_red():
        """
        This function is used to set the LED to red.
        """
        pycom.rgbled(0x7f0000)
    ##
    # set the led to green
    def set_led_green():
        """
        This function is used to set the LED to green.
        """
        pycom.rgbled(0x007f00)



while 1:
    # unit_test_calculate_temp_positive(temp_offset)
    # unit_test_calculate_temp_negative(temp_offset)
    # unit_test_calculate_light_low()
    # unit_test_calculate_light_high()
    # unit_test_calculate_humd(humd_offset)
    # unit_test_construct_payload()
    # unit_test_receive_sensor_value()
    # unit_test_lora_join()
    try:
        s = lora_connection()
        pressure,temp,light,humdity = receive_sensor_value()
        pressure = calculate_pressure(pressure)
        fulltemp,decimaltemp,minus = calculate_temp(temp)
        light = calculate_light(light)
        humdity = calculate_humd(humdity)
        #sends the payload of sensor data over the LoRa network using the socket object s.
        s.send(construct_payload(fulltemp,decimaltemp,pressure,humdity,light,minus))
        time.sleep(send_delay);
    except:
        machine.reset()
