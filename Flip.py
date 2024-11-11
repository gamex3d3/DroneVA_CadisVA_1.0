import tellopy

# Connect to the Tello drone
drone = tellopy.Tello()
drone.connect()

drone.flip_forward()
drone.flip_back()
drone.flip_left()
drone.flip_right()

