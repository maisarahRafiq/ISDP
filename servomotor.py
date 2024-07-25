import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set all pins as output and set servos as PWM
servo1_pin = 13     # GPIO 27
servo2_pin = 15     # GPIO 22
servo3_pin = 16     # GPIO 23
servo4_pin = 18     # GPIO 24
GPIO.setup(servo1_pin, GPIO.OUT)
servo1 = GPIO.PWM(servo1_pin, 50)  # GPIO 27
GPIO.setup(servo2_pin, GPIO.OUT)
servo2 = GPIO.PWM(servo2_pin, 50)  # GPIO 22
GPIO.setup(servo3_pin, GPIO.OUT)
servo3 = GPIO.PWM(servo3_pin, 50)  # GPIO 23
GPIO.setup(servo4_pin, GPIO.OUT)
servo4 = GPIO.PWM(servo4_pin, 50)  # GPIO 24

# Start PWM running, but with value of 0 (pulse off)
servo1.start(0)
servo2.start(0)
servo3.start(0)
servo4.start(0)
print("Waiting for 2 seconds")
time.sleep(2)

# Let's move the servo
print("Rotating servo1 to 7 duty cycle")
servo1.ChangeDutyCycle(7)
time.sleep(2)
servo1.ChangeDutyCycle(0)

time.sleep(2)

# Move all servos together
print("Moving all servos")
servo1.ChangeDutyCycle(2)
servo2.ChangeDutyCycle(7)
servo3.ChangeDutyCycle(7)
servo4.ChangeDutyCycle(2)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
servo2.ChangeDutyCycle(0)
servo3.ChangeDutyCycle(0)
servo4.ChangeDutyCycle(0)

time.sleep(2)

print("Moving all servos again")
servo1.ChangeDutyCycle(2)
servo2.ChangeDutyCycle(7)
servo3.ChangeDutyCycle(7)
servo4.ChangeDutyCycle(2)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)
servo2.ChangeDutyCycle(0)
servo3.ChangeDutyCycle(0)
servo4.ChangeDutyCycle(0)

time.sleep(2)

# Clean things up at the end
servo1.stop()
servo2.stop()
servo3.stop()
servo4.stop()
GPIO.cleanup()
print("Goodbye")
