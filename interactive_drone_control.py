import RPi.GPIO as GPIO
import time
from datetime import datetime
import threading

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

def log(message):
    """Log the message with a timestamp"""
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    print("---")

def set_servo_angle(servo, angle):
    """Set servo to a specific angle"""
    duty = min(max(angle / 18 + 2, 2), 12)  # Constrain duty cycle to 2-12%
    servo.ChangeDutyCycle(duty)
    # Commenting out the print statement for servo angle
    # log(f"Set servo to angle {angle}")

def rotate_servo(servo, start_angle, end_angle, duration, steps):
    """Rotate the servo from start_angle to end_angle over a duration"""
    step = 10 if start_angle < end_angle else -10
    for angle in range(start_angle, end_angle, step):
        # Ensure angle is within bounds
        angle = min(max(angle, 0), 180)
        set_servo_angle(servo, angle)
        time.sleep(duration / steps)
    # Set the final angle explicitly to ensure it ends at the correct position
    set_servo_angle(servo, end_angle)

def move_drone(movement, speed='normal'):
    """Control drone movement with parallel servo operation"""
    log(f"Executing {movement} at {speed} speed...")
    
    duration = 5 if speed == 'normal' else 2.5
    steps = 36  # For smoother 360-degree rotation

    def parallel_rotate(servo, start_angle, end_angle):
        rotate_servo(servo, start_angle, end_angle, duration, steps)

    threads = []
    
    if movement == "move_down":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo2, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo3, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo4, 0, 180))
            ]
    elif movement == "move_up":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo2, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo3, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo4, 180, 0))
            ]
    elif movement == "move_forward":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo2, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo3, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo4, 0, 180))
            ]
    elif movement == "move_backward":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo2, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo3, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo4, 180, 0))
            ]
    elif movement == "bend_left":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo2, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo3, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo4, 180, 0))
            ]
    elif movement == "bend_right":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo2, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo3, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo4, 0, 180))
            ]
    elif movement == "rotate_left":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo2, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo3, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo4, 0, 180))
            ]
    elif movement == "rotate_right":
        for _ in range(3):
            threads = [
                threading.Thread(target=parallel_rotate, args=(servo1, 180, 0)),
                threading.Thread(target=parallel_rotate, args=(servo2, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo3, 0, 180)),
                threading.Thread(target=parallel_rotate, args=(servo4, 180, 0))
            ]
    elif movement == "hover":
        for _ in range(3):
            set_servo_angle(servo1, 0)
            set_servo_angle(servo2, 0)
            set_servo_angle(servo3, 0)
            set_servo_angle(servo4, 0)
            time.sleep(duration / 3)
        return  # No need for threading in hover

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def get_user_input(prompt):
    """Get user input (y/n) for decision points"""
    while True:
        response = input(prompt + " (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' or 'n'.")

def simulate_drone():
    log("Drone simulation started")
    
    log("Power On")
    move_drone("hover", 'normal')  # Initial hover to show power on
    
    battery_low = False
    drone_landed = False
    count = 0
    
    while not drone_landed:
        battery_low = get_user_input("Is battery low?")
        
        if battery_low:
            log("Battery Low - Initiating landing sequence")
            move_drone("move_down", 'normal')
            drone_landed = True
            break
        
        log("Moving Upwards")
        move_drone("move_up", 'normal')
        
        log("Image Processing")
        obstacle_detected = get_user_input("Is an obstacle detected?")
        
        if obstacle_detected:
            log("Obstacle detected, moving backwards")
            move_drone("move_backward", 'normal')
        else:
            is_speaker = get_user_input("Is it a speaker?")
            
            if is_speaker:
                log("Speaker detected")
                log("Frequency Processing")
                violet_sound_detected = get_user_input("Is violet sound detected?")
                
                if violet_sound_detected:
                    log("Violet sound detected")
                    log("Moving Forward")
                    move_drone("move_forward", 'high')
                    log("Frequency Response and ANC Speaker activated")
                    log("Detecting distance")
                    move_drone("hover", 'normal')
                    
                    db_reduced = get_user_input("Is dB reduced?")
                    if db_reduced:
                        log("dB reduced, hovering for 30s")
                        move_drone("hover", 'normal')
                        time.sleep(30)
                        count += 1
                        
                        if count >= 3:
                            log("Count reached 3, initiating landing")
                            move_drone("move_down", 'normal')
                            drone_landed = True
                    else:
                        log("dB not reduced, continuing normal operation")
                        move_drone("rotate_left", 'normal')
                        move_drone("rotate_right", 'normal')
                else:
                    log("No violet sound detected, continuing normal operation")
                    move_drone("hover", 'normal')
            else:
                log("No speaker detected, continuing normal operation")
                move_drone("hover", 'normal')
        
        if not drone_landed:
            log("Transmitting data: Battery life, GPS, Live Streaming, Decibel meter")
            move_drone("hover", 'normal')
        
        if not drone_landed:
            drone_landed = get_user_input("Should the drone land now?")
    
    log("Landing sequence initiated")
    move_drone("move_down", 'normal')
    log("Drone landed successfully")

# Run the simulation
try:
    simulate_drone()
except KeyboardInterrupt:
    log("Simulation interrupted by user")
finally:
    # Clean up
    servo1.stop()
    servo2.stop()
    servo3.stop()
    servo4.stop()
    GPIO.cleanup()
    log("GPIO cleaned up")
