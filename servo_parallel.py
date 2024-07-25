import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define servo pins
servo1_pin = 13     # GPIO 27
servo2_pin = 15     # GPIO 22
servo3_pin = 16     # GPIO 23
servo4_pin = 18     # GPIO 24

# Set up GPIO pins
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(servo3_pin, GPIO.OUT)
GPIO.setup(servo4_pin, GPIO.OUT)

# Create PWM objects for each servo
servo1 = GPIO.PWM(servo1_pin, 50)  # GPIO 27
servo2 = GPIO.PWM(servo2_pin, 50)  # GPIO 22
servo3 = GPIO.PWM(servo3_pin, 50)  # GPIO 23
servo4 = GPIO.PWM(servo4_pin, 50)  # GPIO 24

# Start PWM
servo1.start(0)
servo2.start(0)
servo3.start(0)
servo4.start(0)

def set_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)

try:
    while True:
        # Example: Move all servos from 0 to 180 degrees
        for angle in range(0, 181, 10):
            set_angle(servo1, angle)
            set_angle(servo2, angle)
            set_angle(servo3, angle)
            set_angle(servo4, angle)
        
        # Move back from 180 to 0 degrees
        for angle in range(180, -1, -10):
            set_angle(servo1, angle)
            set_angle(servo2, angle)
            set_angle(servo3, angle)
            set_angle(servo4, angle)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Clean up
    servo1.stop()
    servo2.stop()
    servo3.stop()
    servo4.stop()
    GPIO.cleanup()
