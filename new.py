import RPi.GPIO as GPIO

# Set up GPIO mode (this should match the mode used in your main program)
GPIO.setmode(GPIO.BOARD)

# Clean up all GPIO pins
GPIO.cleanup()

print("GPIO cleanup completed")
