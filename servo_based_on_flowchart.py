import time
import random

class SimulatedServo:
    def __init__(self, name):
        self.name = name
        self.angle = 0

    def set_angle(self, angle):
        self.angle = angle
        print(f"Servo {self.name} moved to {self.angle} degrees")

class SimulatedDrone:
    def __init__(self):
        self.battery = 100
        self.position = 0  # 0: ground, 1: air
        self.count = 0
        self.servos = {
            'move': SimulatedServo('move'),
            'camera': SimulatedServo('camera'),
            'audio': SimulatedServo('audio'),
            'hover': SimulatedServo('hover')
        }

    def simulate_action(self, action, duration=1):
        print(f"Simulating action: {action}")
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

    def check_battery(self):
        self.battery -= random.randint(1, 5)
        return self.battery > 20

    def detect_obstacle(self):
        return random.random() < 0.3  # 30% chance of obstacle

    def detect_violet_sound(self):
        return random.random() < 0.2  # 20% chance of violet sound

    def detect_speaker(self):
        return random.random() < 0.4  # 40% chance of speaker

    def reduce_db(self):
        return random.random() < 0.8  # 80% chance of successful dB reduction

def drone_logic():
    print("START")
    print("Power On")
    
    drone = SimulatedDrone()
    drone_landed = False

    while not drone_landed:
        print(f"\nCurrent battery: {drone.battery}%")
        print("Checking battery...")
        if drone.check_battery():
            print("Battery OK")
            drone.simulate_action("Move Upwards")
            drone.position = 1
            
            print("Processing image and audio")
            drone.simulate_action("Image Processing", 0.5)
            drone.simulate_action("Audio Processing", 0.5)
            
            if drone.detect_obstacle():
                print("Obstacle detected")
                drone.simulate_action("Detect distance")
                drone.simulate_action("Move Backwards")
            elif drone.detect_violet_sound():
                print("Violet sound detected")
            else:
                print("No obstacle or violet sound")
                if drone.detect_speaker():
                    print("Speaker detected")
                    drone.simulate_action("Detect distance")
                    drone.simulate_action("Move Forward")
                    drone.simulate_action("ANC Speaker")
                    
                    if drone.reduce_db():
                        print("dB reduced")
                        drone.simulate_action("Hover", 3)
                        drone.count += 1
                        print(f"Count: {drone.count}")
                        
                        if drone.count >= 3:
                            print("Count reached 3, initiating landing")
                            drone.simulate_action("Land")
                            drone_landed = True
                    else:
                        print("Failed to reduce dB, continuing search")
                else:
                    print("No speaker detected, continuing search")
        else:
            print("Battery Low, initiating landing")
            drone.simulate_action("Land")
            drone_landed = True
        
        print("Transmitting data to telemetry")
        print("Updating battery life, GPS, live streaming, decibel meter")

    print("Drone landed")
    print("END")

# Run multiple simulations
for i in range(3):
    print(f"\n\nSimulation {i+1}")
    print("="*20)
    drone_logic()
    time.sleep(2)
