#Import libraries
import RPi.GPIO as GPIO
import time

#Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

#Set pin all as outou, and set servol as pin as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)
GPIO.setup(12,GPIO.OUT)
servo2 = GPIO.PWM(12,50)
GPIO.setup(13,GPIO.OUT)
servo3 = GPIO.PWM(13,50)
GPIO.setup(15,GPIO.OUT)
servo4 = GPIO.PWM(15,50)

#Start PWM running, but with value of 0 (pulse off)
servo1.start(0)
servo2.start(0)
servo3.start(0)
servo4.start(0)
print("Waiting for 2 seconds")
time.sleep(2)

#Let's move the servo
print("Rotating 180 degrees in 10 steps")

#Define variable duty
servo1.ChangeDutyCycle(7)
time.sleep(2)
servo1.ChangeDutyCycle(0)

time.sleep(2)

#Turn back to 90 degrees
servo2.ChangeDutyCycle(7)
servo1.ChangeDutyCycle(2)
servo3.ChangeDutyCycle(7)
servo4.ChangeDutyCycle(2)
time.sleep(0.5)
servo2.ChangeDutyCycle(0)
servo1.ChangeDutyCycle(0)
servo3.ChangeDutyCycle(0)
servo4.ChangeDutyCycle(0)

time.sleep(2)

servo2.ChangeDutyCycle(7)
servo1.ChangeDutyCycle(2)
servo3.ChangeDutyCycle(7)
servo4.ChangeDutyCycle(2)
time.sleep(0.5)
servo2.ChangeDutyCycle(0)
servo1.ChangeDutyCycle(0)
servo3.ChangeDutyCycle(0)
servo4.ChangeDutyCycle(0)

time.sleep(2)


#Clean things up at the end
servo1.stop()
servo2.stop()
servo3.stop()
servo4.stop()
GPIO.cleanup()
print("Goodbye")