import tellopy

# Connect to the Tello drone
drone = tellopy.Tello()
drone.connect()

for i in range(10):
    drone.flip_forward(1)
    drone.counter_clockwise(36)

