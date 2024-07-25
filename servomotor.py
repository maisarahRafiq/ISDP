import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)

# Define servo pins
servo_pins = {
    1: 13,  # GPIO 27
    2: 15,  # GPIO 22
    3: 16,  # GPIO 23
    4: 18   # GPIO 24
}

def setup_servo(pin):
    GPIO.setup(pin, GPIO.OUT)
    return GPIO.PWM(pin, 50)

def test_servo(servo, servo_num):
    print(f"Testing Servo {servo_num} on pin {servo_pins[servo_num]}")
    servo.start(0)
    
    for angle in [0, 90, 180, 90, 0]:
        duty = angle / 18 + 2
        print(f"Moving Servo {servo_num} to {angle} degrees (duty cycle: {duty:.2f})")
        servo.ChangeDutyCycle(duty)
        time.sleep(1)
    
    servo.stop()
    print(f"Finished testing Servo {servo_num}")

try:
    for servo_num in servo_pins:
        input(f"Press Enter to test Servo {servo_num} on pin {servo_pins[servo_num]}...")
        
        servo = setup_servo(servo_pins[servo_num])
        test_servo(servo, servo_num)
        
        GPIO.cleanup(servo_pins[servo_num])
        
        response = input("Did the correct servo move? (yes/no): ").lower()
        if response != 'yes':
            print(f"Please check the wiring for Servo {servo_num} on pin {servo_pins[servo_num]}")
        
        print("\n")

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    GPIO.cleanup()
    print("GPIO cleanup completed")
