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
servo1 = GPIO.PWM(servo1_pin, 50)
servo2 = GPIO.PWM(servo2_pin, 50)
servo3 = GPIO.PWM(servo3_pin, 50)
servo4 = GPIO.PWM(servo4_pin, 50)

def test_servo(servo, servo_name):
    print(f"Testing {servo_name}")
    servo.start(0)
    
    for angle in [0, 90, 180, 90, 0]:
        duty = angle / 18 + 2
        print(f"Moving {servo_name} to {angle} degrees (duty cycle: {duty:.2f})")
        servo.ChangeDutyCycle(duty)
        time.sleep(1)
    
    servo.stop()
    print(f"Finished testing {servo_name}\n")

try:
    test_servo(servo1, "Servo 1")
    time.sleep(2)
    
    test_servo(servo2, "Servo 2")
    time.sleep(2)
    
    test_servo(servo3, "Servo 3")
    time.sleep(2)
    
    test_servo(servo4, "Servo 4")

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Clean up
    GPIO.cleanup()
    print("GPIO cleanup completed")
