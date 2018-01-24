# This Code uses the:
# * Adafruit LCD backpack using MCP23008 I2C expander 
# * Maxbotic LV-EZ1 Ultrasonic Sensor
#
# Tested with the Trinket M0
# The ultrasonic sensor and pin use should be Gemma M0 compatible
# This sketch reads the LV-EZ1 by pulse count 
# Then prints the distance to the LCD and python console
#
# The circuit:
# * 5V to Trinket M0 USB or BAT pin, I2C Backpack 5V and EZ1 +5
# * GND to Trinket M0 GND pin, I2C Backpack GND and EZ1 GND
# * Display I2C Backpack SLK to Trinket GPIO #2 
# * Display I2C backpack SDA to Trinket GPIO #0 
# * LV-EZ1 Ultrasonic Sensor PW pin to Trinket GPIO #1 
# * Backlight can be hard wired by connecting LCD pin 16, 17 or 18 to GND

import board
import busio
import time
import pulseio
import adafruit_character_lcd

ez1pin = board.D1    # Trinket GPIO #1   

# i2c LCD initialize bus and class
i2c = busio.I2C(board.SCL, board.SDA)
cols = 16
rows = 2
lcd = adafruit_character_lcd.Character_LCD_I2C(i2c, cols, rows)

# calculated mode or median distance
mode_result = 0 

# pulseio can store multiple pulses 
# read in time for pin to transition
samples = 18
pulses = pulseio.PulseIn(board.D1, maxlen=samples) 

# sensor reads which are in range will be stored here
rangevalue = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# 25ms sensor power up pause
time.sleep(.25)

# EZ1 ultrasonic sensor is measuring "time of flight" 
# * convert time of flight into distance
# * centimeters (divide by 58mS) 
# * inches (divide by 147mS)
# * centimeter is default output, flip comments for inches
def tof_to_distance(tof):
#    convert_to_inches = 147
    convert_to_cm = 58

#    inches = tof / convert_to_inches
    cm = tof / convert_to_cm

#   return inches
    return cm

# find the mode (most common value reported)
# will return median (center of sorted list)
# should mode not be found
def mode(x, n):

    maxcount = 0
    mode = 0
    bimodal = 0
    prevcount = 0
    counter = 0
    i = 0

    while ( i < ( n - 1 ) ):
        prevcount = counter
        counter = 0

        while ( ( x[i] ) == ( x[i+1] ) ):
            counter += 1
            i += 1

        if ( ( counter > prevcount ) and ( counter > maxcount ) ):
            mode = x[i]
            maxcount = counter
            bimodal = 0

        if ( counter == 0 ):
            i += 1

        # If the dataset has 2 or more modes.
        if ( counter == maxcount ):        
            bimodal = 1

        # Return the median if there is no mode.
        if ( ( mode == 0 ) or ( bimodal == 1 ) ):   
            mode = x [ int ( n / 2 ) ]

        return mode

while True:

    # wait between samples
    time.sleep(.5)

    if ( len(pulses) == samples ):
        j = 0     # rangevalue array counter

        # only save the values within range
        # range readings take 49mS
        # pulse width is .88mS to 37.5mS
        for i in range( 0, samples ):
            tof = pulses[i] # time of flight - PWM HIGH

            if ( ( tof > 880 ) and ( tof < 37500 ) ):
                if ( j < len(rangevalue) ): 
                    rangevalue[j] = tof_to_distance(tof)
                    j += 1


        # clear pulse samples
        pulses.clear()  # clear all values in pulses[]

        # sort samples
        rangevalue = sorted(rangevalue)

        # returns mode or median
        mode_result = int(mode(rangevalue, len(rangevalue)))

        # python console prints both centimeter and inches distance
        cm2in = .393701 
        mode_result_in = mode_result * cm2in
        print(mode_result, "cm", "\t\t", int(mode_result_in), "in")

        # result must be in char/string format for LCD printing
        digit_string = str(mode_result)

        lcd.clear()
        lcd.message("Range: ")  # write to LCD
        lcd.message("    ")
        lcd.message(digit_string)
        lcd.message("cm")
  
        time.sleep(2)
