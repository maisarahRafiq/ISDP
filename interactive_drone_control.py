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

def set_servo_angle(servo, angle):
    """Set servo to a specific angle"""
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)

def move_drone(movement, duration=3):
    """Control drone movement with more pronounced and longer-lasting movements"""
    print(f"Executing {movement}...")
    if movement == "move_down":
        for _ in range(3):  # Repeat movement for emphasis
            set_servo_angle(servo1, 0)
            set_servo_angle(servo2, 0)
            set_servo_angle(servo3, 90)
            set_servo_angle(servo4, 90)
            time.sleep(duration/3)
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 45)
            time.sleep(duration/3)
    elif movement == "move_up":
        for _ in range(3):
            set_servo_angle(servo1, 90)
            set_servo_angle(servo2, 90)
            set_servo_angle(servo3, 0)
            set_servo_angle(servo4, 0)
            time.sleep(duration/3)
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 45)
            time.sleep(duration/3)
    elif movement == "move_forward":
        for _ in range(3):
            set_servo_angle(servo1, 90)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 90)
            set_servo_angle(servo4, 45)
            time.sleep(duration/3)
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 45)
            time.sleep(duration/3)
    elif movement == "move_backward":
        for _ in range(3):
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 90)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 90)
            time.sleep(duration/3)
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 45)
            time.sleep(duration/3)
    elif movement == "rotate_left":
        for _ in range(3):
            set_servo_angle(servo1, 0)
            set_servo_angle(servo2, 90)
            set_servo_angle(servo3, 90)
            set_servo_angle(servo4, 0)
            time.sleep(duration/3)
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 45)
            time.sleep(duration/3)
    elif movement == "rotate_right":
        for _ in range(3):
            set_servo_angle(servo1, 90)
            set_servo_angle(servo2, 0)
            set_servo_angle(servo3, 0)
            set_servo_angle(servo4, 90)
            time.sleep(duration/3)
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 45)
            time.sleep(duration/3)
    elif movement == "hover":
        for _ in range(3):
            set_servo_angle(servo1, 45)
            set_servo_angle(servo2, 45)
            set_servo_angle(servo3, 45)
            set_servo_angle(servo4, 45)
            time.sleep(duration)

def get_user_input(prompt):
    """Get user input (y/n) for decision points"""
    while True:
        response = input(prompt + " (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' or 'n'.")

def simulate_drone():
    print("Drone simulation started")
    
    print("Power On")
    move_drone("hover", 5)  # Initial hover to show power on
    
    battery_low = False
    drone_landed = False
    count = 0
    
    while not drone_landed:
        battery_low = get_user_input("Is battery low?")
        
        if battery_low:
            print("Battery Low - Initiating landing sequence")
            move_drone("move_down", 5)
            drone_landed = True
            break
        
        print("Moving Upwards")
        move_drone("move_up", 5)
        
        obstacle_detected = get_user_input("Is an obstacle detected?")
        
        if obstacle_detected:
            print("Obstacle detected, moving backwards")
            move_drone("move_backward", 5)
        else:
            is_speaker = get_user_input("Is it a speaker?")
            
            if is_speaker:
                print("Speaker detected")
                violet_sound_detected = get_user_input("Is violet sound detected?")
                
                if violet_sound_detected:
                    print("Violet sound detected")
                    move_drone("move_forward", 5)
                    print("Frequency Response and ANC Speaker activated")
                    move_drone("hover", 5)
                    
                    db_reduced = get_user_input("Is dB reduced?")
                    if db_reduced:
                        print("dB reduced, hovering for demonstration")
                        move_drone("hover", 10)
                        count += 1
                        
                        if count >= 3:
                            print("Count reached 3, initiating landing")
                            move_drone("move_down", 5)
                            drone_landed = True
                    else:
                        print("dB not reduced, continuing normal operation")
                        move_drone("rotate_left", 5)
                        move_drone("rotate_right", 5)
                else:
                    print("No violet sound detected, continuing normal operation")
                    move_drone("hover", 3)
            else:
                print("No speaker detected, continuing normal operation")
                move_drone("hover", 3)
        
        if not drone_landed:
            print("Transmitting data: Battery life, GPS, Live Streaming, Decibel meter")
            move_drone("hover", 3)
        
        if not drone_landed:
            drone_landed = get_user_input("Should the drone land now?")
    
    print("Landing sequence initiated")
    move_drone("move_down", 5)
    print("Drone landed successfully")

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
