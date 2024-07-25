import RPi.GPIO as GPIO
import time
import threading

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define servo pins
servo_pins = {
    'servo1': 13,  # GPIO 27
    'servo2': 15,  # GPIO 22
    'servo3': 16,  # GPIO 23
    'servo4': 18   # GPIO 24
}

# Set up GPIO pins and create PWM objects
servos = {}
for name, pin in servo_pins.items():
    GPIO.setup(pin, GPIO.OUT)
    servos[name] = GPIO.PWM(pin, 50)
    servos[name].start(0)

def set_angle(servo, angle):
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)

def move_servo(servo_name, angles):
    for angle in angles:
        set_angle(servos[servo_name], angle)

try:
    while True:
        # Move from 0 to 180 degrees
        threads = []
        for servo_name in servos:
            thread = threading.Thread(target=move_servo, args=(servo_name, range(0, 181, 10)))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Move from 180 to 0 degrees
        threads = []
        for servo_name in servos:
            thread = threading.Thread(target=move_servo, args=(servo_name, range(180, -1, -10)))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    # Clean up
    for servo in servos.values():
        servo.stop()
    GPIO.cleanup()
