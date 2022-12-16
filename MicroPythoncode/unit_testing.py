
def unit_test_calculate_pressure():
    # Import the calculate_pressure() function from the main module
    from main import calculate_pressure

    # Test input
    pres = 100400
    # Expected output
    expected_value = 104

    # Compare the function's output to the expected value
    if(calculate_pressure(pres) == expected_value):
        # If the output matches the expected value, the unit test has passed
        print("unit test calculate pressure is GOOD")
    else:
        # If the output does not match the expected value, the unit test has failed
        print("unit test caclulate pressure if FAILED")


def unit_test_calculate_temp_positive(temp_offset):
    # Import the calculate_temp() function from the main module
    from main import calculate_temp

    # Test input
    temp = 20.7
    # Expected output
    expected_value_fulltemp = 20 + temp_offset
    expected_value_decimaltemp = 7
    expected_value_minus = 0

    # Get the function's output
    fulltemp,decimaltemp,minus = calculate_temp(temp)

    # Compare the function's output to the expected values
    if(fulltemp == expected_value_fulltemp and decimaltemp == expected_value_decimaltemp and minus == expected_value_minus):
        # If the output matches the expected values, the unit test has passed
        print("unit test calculate temperature positive is GOOD")
    else:
        # If the output does not match the expected values, the unit test has failed
        print("unit test calculate temperature positive if FAILED")


def unit_test_calculate_temp_negative(temp_offset):
    # Import the calculate_temp function from the main module
    from main import calculate_temp

    # Set the input temperature to -20.7
    temp = -20.7

    # Calculate the expected output values based on the input temperature and temp_offset
    expected_value_fulltemp = 20 + temp_offset
    expected_value_decimaltemp = 7
    expected_value_minus = 1

    # Call the calculate_temp function with the input temperature
    fulltemp, decimaltemp, minus = calculate_temp(temp)

    # Compare the returned values to the expected output values
    if fulltemp == expected_value_fulltemp and decimaltemp == expected_value_decimaltemp and minus == expected_value_minus:
        # If all values match, print a success message
        print("unit test calculate temperature positive is GOOD")
    else:
        # If any values do not match, print a failure message
        print("unit test calculate temperature positive if FAILED")


def unit_test_calculate_light_low():
    # Import the calculate_light function from the main module
    from main import calculate_light

    # Set the input light value to 100
    light = 100

    # Set the expected output value to 100
    expected_value = 100

    # Call the calculate_light function with the input light value
    reallight = calculate_light(light)

    # Compare the returned value to the expected output value
    if reallight == expected_value:
        # If the values match, print a success message
        print("unit test calculate low light is GOOD")
    else:
        # If the values do not match, print a failure message
        print("unit test calculate low light if FAILED")


def unit_test_calculate_light_high():
    # Import the calculate_light function from the main module
    from main import calculate_light

    # Import the math module
    import math

    # Set the input light value to 350
    light = 350

    # Calculate the expected output value using the math.log function
    expected_value = int(round(math.log(light,1.04),0))

    # Call the calculate_light function with the input light value
    reallight = calculate_light(light)

    # Compare the returned value to the expected output value
    if reallight == expected_value:
        # If the values match, print a success message
        print("unit test calculate high light is GOOD")
    else:
        # If the values do not match, print a failure message
        print("unit test calculate high light if FAILED")


def unit_test_calculate_humd(hum_offset):
    # Import the calculate_humd function from the main module
    from main import calculate_humd

    # Set the input humidity value to 50
    hum = 50

    # Calculate the expected output value using the hum_offset parameter
    expected_value = hum * hum_offset

    # Call the calculate_humd function with the input humidity value
    calculated_value = calculate_humd(hum)

    # Compare the returned value to the expected output value
    if expected_value == calculated_value:
        # If the values match, print a success message
        print("unit test calculate humdity is GOOD")
    else:
        # If the values do not match, print a failure message
        print("unit test calculate humdity if FAILED")


def unit_test_construct_payload():
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
    # Import the lora_connection function from the main module
    from main import lora_connection

    # Print a message to the console
    print("trying to connect to lora")
    print("open your The Things Network application to check if the sensor can join")

    # Call the lora_connection function
    lora_connection()


def unit_test_receive_sensor_value():
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
