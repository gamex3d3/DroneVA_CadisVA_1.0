import tellopy

# Connect to the Tello drone
drone = tellopy.Tello()
drone.connect()

drone.take_picture()