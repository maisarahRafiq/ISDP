import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)

# Define servo pins
servo1_pin = 13  # GPIO 27
servo2_pin = 15  # GPIO 22
servo3_pin = 18  # GPIO 24
servo4_pin = 16  # GPIO 23

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

# Start PWM
servo1.start(0)
servo2.start(0)
servo3.start(0)
servo4.start(0)

def set_servo_speed(servo, speed):
    """Set servo speed (duty cycle)"""
    if speed == "normal":
        duty = 7.5  # Adjust as needed
    elif speed == "high":
        duty = 10  # Adjust as needed
    servo.ChangeDutyCycle(duty)

def move_drone(movement, speed="normal"):
    """Control drone movement based on the control diagram"""
    if movement == "move_down":
        set_servo_speed(servo1, speed)
        set_servo_speed(servo2, speed)
        set_servo_speed(servo3, "normal")
        set_servo_speed(servo4, "normal")
    elif movement == "move_up":
        set_servo_speed(servo1, "normal")
        set_servo_speed(servo2, "normal")
        set_servo_speed(servo3, speed)
        set_servo_speed(servo4, speed)
    elif movement == "move_forward":
        set_servo_speed(servo1, speed)
        set_servo_speed(servo2, "normal")
        set_servo_speed(servo3, speed)
        set_servo_speed(servo4, "normal")
    elif movement == "move_backward":
        set_servo_speed(servo1, "normal")
        set_servo_speed(servo2, speed)
        set_servo_speed(servo3, "normal")
        set_servo_speed(servo4, speed)
    elif movement == "bend_left":
        set_servo_speed(servo1, "normal")
        set_servo_speed(servo2, speed)
        set_servo_speed(servo3, "normal")
        set_servo_speed(servo4, speed)
    elif movement == "bend_right":
        set_servo_speed(servo1, speed)
        set_servo_speed(servo2, "normal")
        set_servo_speed(servo3, speed)
        set_servo_speed(servo4, "normal")
    elif movement == "rotate_left":
        set_servo_speed(servo1, "normal")
        set_servo_speed(servo2, speed)
        set_servo_speed(servo3, speed)
        set_servo_speed(servo4, "normal")
    elif movement == "rotate_right":
        set_servo_speed(servo1, speed)
        set_servo_speed(servo2, "normal")
        set_servo_speed(servo3, "normal")
        set_servo_speed(servo4, speed)

def get_user_input(prompt):
    """Get user input (y/n) for decision points"""
    while True:
        response = input(prompt + " (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' or 'n'.")

def simulate_drone():
    print("Drone simulation started")
    
    # Power On
    print("Power On")
    
    battery_low = False
    drone_landed = False
    count = 0
    
    while not drone_landed:
        # Check battery
        battery_low = get_user_input("Is battery low?")
        
        if battery_low:
            print("Battery Low")
            drone_landed = True
            break
        
        # Move Upwards
        print("Moving Upwards")
        move_drone("move_up", "high")
        time.sleep(2)
        
        # Image and Audio Processing
        obstacle_detected = get_user_input("Is an obstacle detected?")
        
        if obstacle_detected:
            print("Obstacle detected, moving backwards")
            move_drone("move_backward", "high")
            time.sleep(2)
        else:
            violet_sound_detected = get_user_input("Is violet sound detected?")
            
            if violet_sound_detected:
                print("Violet sound detected")
                move_drone("move_forward")
                time.sleep(1)
                print("Frequency Response")
                time.sleep(1)
                print("ANC Speaker activated")
                time.sleep(1)
                
                db_reduced = get_user_input("Is dB reduced?")
                if db_reduced:
                    print("dB reduced, hovering for 30s")
                    move_drone("move_up")  # Hover
                    time.sleep(30)
                    count += 1
                    
                    if count >= 3:
                        print("Count reached 3, landing")
                        drone_landed = True
                else:
                    print("dB not reduced, continuing")
        
        # Data Transmission
        print("Transmitting data: Battery life, GPS, Live Streaming, Decibel meter")
        time.sleep(1)
        
        # Check if drone has landed
        drone_landed = get_user_input("Has the drone landed?")
    
    # Landing
    print("Landing")
    move_drone("move_down", "normal")
    time.sleep(3)
    print("Drone landed")

# Run the simulation
try:
    simulate_drone()
except KeyboardInterrupt:
    print("Simulation interrupted by user")
finally:
    # Clean up
    servo1.stop()
    servo2.stop()
    servo3.stop()
    servo4.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
