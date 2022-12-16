
def unit_test_calculate_pressure():
    from main import calculate_pressure
    pres = 100400
    expected_value = 104
    if(calculate_pressure(pres) == expected_value):
        print("unit test calculate pressure is GOOD")
    else:
        print("unit test caclulate pressure if FAILED")

def unit_test_calculate_temp_positive(temp_offset):
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
    from main import calculate_temp
    temp = -20.7
    expected_value_fulltemp = 20 + temp_offset
    expected_value_decimaltemp = 7
    expected_value_minus = 1
    fulltemp,decimaltemp,minus = calculate_temp(temp)
    if(fulltemp == expected_value_fulltemp and decimaltemp == expected_value_decimaltemp and minus == expected_value_minus):
        print("unit test calculate temperature positive is GOOD")
    else:
        print("unit test calculate temperature positive if FAILED")

def unit_test_calculate_light_low():
    from main import calculate_light
    light = 100
    expected_value = 100
    reallight = calculate_light(light)
    if(reallight == expected_value):
        print("unit test calculate low light is GOOD")
    else:
        print("unit test calculate low light if FAILED")

def unit_test_calculate_light_high():
    from main import calculate_light
    import math
    light = 350
    expected_value = int(round(math.log(light,1.04),0))
    reallight = calculate_light(light)
    if(reallight == expected_value):
        print("unit test calculate high light is GOOD")
    else:
        print("unit test calculate high light if FAILED")

def unit_test_calculate_humd(hum_offset):
    from main import calculate_humd
    hum = 50
    expected_value = hum * hum_offset
    calculated_value = calculate_humd(hum)
    if(expected_value == calculated_value):
        print("unit test calculate humdity is GOOD")
    else:
        print("unit test calculate humdity if FAILED")

def unit_test_construct_payload():
    from main import construct_payload
    import ustruct
    fulltemp = 10
    decimaltemp = 5
    pressure = 50
    humdity = 60
    light = 100
    minus = 0
    expected_value = b'2\n\x05d<\x00'
    real_value = construct_payload(fulltemp,decimaltemp,pressure,humdity,light,minus)
    if(expected_value == real_value):
        print("unit test construct_payload is GOOD")
    else:
        print("unit test construct_payload if FAILED")

def unit_test_lora_join():
    from main import lora_connection
    print("trying to connect to lora")
    print("open your The Things Network application to check if the sensor can join")
    lora_connection()

def unit_test_receive_sensor_value():
    from main import receive_sensor_value
    print("trying to receive sensor value")
    print("check if sensor values are valid for your ambiant")
    pressure,temp,light,humdity = receive_sensor_value()
    print("pressure: " + str(pressure))
    print("temperature: " + str(temp))
    print("light: " + str(light))
    print("humdity: " + str(humdity))
