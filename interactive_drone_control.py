import time
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

class Servo:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.angle = 0
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz frequency
        self.pwm.start(0)

    def set_angle(self, angle):
        self.angle = angle
        duty = angle / 18 + 2
        self.pwm.ChangeDutyCycle(duty)
        print(f"Servo {self.name} moved to {self.angle} degrees")

class Drone:
    def __init__(self):
        self.battery = 100
        self.position = 0  # 0: ground, 1: air
        self.count = 0
        self.servos = {
            'move': Servo('move', 13),    # GPIO 27
            'camera': Servo('camera', 15),  # GPIO 22
            'audio': Servo('audio', 16),   # GPIO 23
            'hover': Servo('hover', 18)    # GPIO 24
        }

    def perform_action(self, action, duration=1):
        print(f"Performing action: {action}")
        if action == "Move Upwards":
            self.servos['move'].set_angle(180)
        elif action == "Move Backwards":
            self.servos['move'].set_angle(0)
        elif action == "Move Forward":
            self.servos['move'].set_angle(90)
        elif action == "Image Processing":
            self.servos['camera'].set_angle(90)
        elif action == "Audio Processing":
            self.servos['audio'].set_angle(90)
        elif action == "Hover":
            self.servos['hover'].set_angle(90)
        elif action == "Land":
            self.servos['move'].set_angle(0)
            self.servos['hover'].set_angle(0)
        time.sleep(duration)
        
        # Reset servos after action (except for landing)
        if action != "Land":
            for servo in self.servos.values():
                servo.set_angle(0)

    def update_battery(self):
        self.battery -= random.randint(1, 5)
        return self.battery > 20

def drone_logic():
    print("START")
    print("Power On")
    
    drone = Drone()
    drone_landed = False

    while not drone_landed:
        print(f"\nCurrent battery: {drone.battery}%")
        print("Checking battery...")
        if drone.update_battery():
            print("Battery OK")
            
            # User input for current situation
            print("\nSelect the current situation:")
            print("1. Takeoff")
            print("2. Obstacle detected")
            print("3. Violet sound detected")
            print("4. Speaker detected")
            print("5. No obstacle or sound detected")
            print("6. Land")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                drone.perform_action("Move Upwards")
                drone.position = 1
                print("Processing image and audio")
                drone.perform_action("Image Processing", 0.5)
                drone.perform_action("Audio Processing", 0.5)
            elif choice == "2":
                print("Obstacle detected")
                drone.perform_action("Detect distance")
                drone.perform_action("Move Backwards")
            elif choice == "3":
                print("Violet sound detected")
            elif choice == "4":
                print("Speaker detected")
                drone.perform_action("Detect distance")
                drone.perform_action("Move Forward")
                drone.perform_action("ANC Speaker")
                print("Attempting to reduce dB...")
                if random.random() < 0.8:  # 80% chance of success
                    print("dB reduced")
                    drone.perform_action("Hover", 3)
                    drone.count += 1
                    print(f"Count: {drone.count}")
                    if drone.count >= 3:
                        print("Count reached 3, initiating landing")
                        drone.perform_action("Land")
                        drone_landed = True
                else:
                    print("Failed to reduce dB, continuing search")
            elif choice == "5":
                print("No obstacle or sound detected, continuing search")
                drone.perform_action("Hover", 1)
            elif choice == "6":
                print("Initiating landing")
                drone.perform_action("Land")
                drone_landed = True
            else:
                print("Invalid choice, please try again")
        else:
            print("Battery Low, initiating landing")
            drone.perform_action("Land")
            drone_landed = True
        
        print("Transmitting data to telemetry")
        print("Updating battery life, GPS, live streaming, decibel meter")

    print("Drone landed")
    print("END")

# Run the drone logic
try:
    drone_logic()
finally:
    # Clean up GPIO at the end
    GPIO.cleanup()
