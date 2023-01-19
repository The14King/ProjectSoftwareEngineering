///\author Twan Wieggers
def unit_test_calculate_pressure():
    """
    Test the calculate_pressure() function from the main module

    @param pres: test input pressure
    @type pres: float
    @return: whether the test passed or failed
    @rtype: str
    """
    from main import calculate_pressure

    pres = 100400
    expected_value = 104

    if(calculate_pressure(pres) == expected_value):
        print("unit test calculate pressure is GOOD")
    else:
        print("unit test caclulate pressure if FAILED")


def unit_test_calculate_temp_positive(temp_offset):
    """
    Test the calculate_temp() function from the main module with positive input temperature

    @param temp: test input temperature
    @type temp: float
    @param temp_offset: the temperature offset
    @type temp_offset: int
    @return: whether the test passed or failed
    @rtype: str
    """
    from main import calculate_temp

    temp = 20.7
    expected_value_fulltemp = 20 + temp_offset
    expected_value_decimaltemp = 7
    expected_value_minus = 0

    fulltemp,decimaltemp,minus = calculate_temp(temp)

    if(fulltemp == expected_value_fulltemp and decimaltemp == expected_value_decimaltemp and minus == expected_value_minus):
        print("unit test calculate temperature positive is GOOD")
    else:
        print("unit test calculate temperature positive if FAILED")


def unit_test_calculate_temp_negative(temp_offset):
    """
    Test the calculate_temp() function from the main module with negative input temperature

    @param temp: test input temperature
    @type temp: float
    @param temp_offset: the temperature offset
    @type temp_offset: int
    @return: whether the test passed or failed
    @rtype: str
    """
    from main import calculate_temp

    temp = -20.7
    expected_value_fulltemp = 20 + temp_offset
    expected_value_decimaltemp = 7
    expected_value_minus = 1

    fulltemp, decimaltemp, minus = calculate_temp(temp)

    if fulltemp == expected_value_fulltemp and decimaltemp == expected_value_decimaltemp and minus == expected_value_minus:
        print("unit test calculate temperature positive is GOOD")
    else:
        print("unit test calculate temperature positive if FAILED")


def unit_test_calculate_light_low():
    """
    Test the calculate_light() function from the main module with a low input light value

    @param light: test input light value
    @type light: int
    @return: whether the test passed or failed
    @rtype: str
    """
    from main import calculate_light

    light = 100
    expected_value = 100

    reallight = calculate_light(light)

    if reallight == expected_value:
        print("unit test calculate low light is GOOD")
    else:
        print("unit test calculate low light if FAILED")


def unit_test_calculate_light_high():
    """
    Test the calculate_light() function from the main module with a high input light value

    @param light: test input light value
    @type light: int
    @return: whether the test passed or failed
    @rtype: str
    """
    from main import calculate_light
    import math

    light = 350
    expected_value = int(round(math.log(light,1.04),0))

    reallight = calculate_light(light)

    if reallight == expected_value:
        print("unit test calculate high light is GOOD")
    else:
        print("unit test calculate high light if FAILED")


def unit_test_calculate_humd():
    """
    Test the calculate_humd() function from the main module

    @param humdity: test input humidity value
    @type humdity: float
    @param humd_offset: the humidity offset
    @type humd_offset: float
    @return: whether the test passed or failed
    @rtype: str
    """
    from main import calculate_humd
    humdity = 50.5
    expected_value = int(humdity*humd_offset)

    realhumd = calculate_humd(humdity)

    if realhumd == expected_value:
        print("unit test calculate humdity is GOOD")
    else:
        print("unit test calculate humdity if FAILED")


def unit_test_construct_payload():
    """
    Test the construct_payload function from the main module.
    """
    # Import the construct_payload function and the ustruct module
    from main import construct_payload
    import ustruct

    # Define test inputs
    fulltemp = 10
    decimaltemp = 5
    pressure = 50
    humdity = 60
    light = 100
    minus = 0

    # Define the expected output for the test
    expected_value = b'2\n\x05d<\x00'

    # Call the construct_payload function with the test inputs
    real_value = construct_payload(fulltemp,decimaltemp,pressure,humdity,light,minus)

    # Compare the returned value to the expected output
    if(expected_value == real_value):
        # If the values are the same, the test passed
        print("unit test construct_payload is GOOD")
    else:
        # If the values are different, the test failed
        print("unit test construct_payload if FAILED")


def unit_test_lora_join():
    """
    Attempts to connect to a LoRa network using the `lora_connection()` function from the main module.

    Prints a message to the console and opens the The Things Network application to check if the sensor can join.
    """
    # Import the lora_connection function from the main module
    from main import lora_connection

    # Print a message to the console
    print("trying to connect to lora")
    print("open your The Things Network application to check if the sensor can join")

    # Call the lora_connection function
    lora_connection()



def unit_test_receive_sensor_value():
    """
    Test function to check if the sensor can receive sensor values.

    @return None
    """
    # Import the receive_sensor_value function from the main module
    from main import receive_sensor_value

    # Print a message to the console
    print("trying to receive sensor value")
    print("check if sensor values are valid for your ambiant")

    # Call the receive_sensor_value function and assign the returned values to variables
    pressure, temp, light, humidity = receive_sensor_value()

    # Print the values returned by the receive_sensor_value function
    print("pressure: " + str(pressure))
    print("temperature: " + str(temp))
    print("light: " + str(light))
    print("humidity: " + str(humidity))
