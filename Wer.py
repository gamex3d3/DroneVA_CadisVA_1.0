import tellopy

# Connect to the Tello drone
drone = tellopy.Tello()
drone.connect()

# Take off
drone.takeoff()

# Move forward 10 meters
drone.flip_forward(10)

# Turn left 90 degrees
drone.counter_clockwise(90)

# Land
drone.land()

# Disconnect from the Tello drone
drone.quit()