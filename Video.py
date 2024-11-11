import cv2
import tellopy

# Connect to the Tello drone
drone = tellopy.Tello()
drone.connect()

# Create a VideoCapture object to capture video from the Tello drone
cap = cv2.VideoCapture(drone.get_video_stream())

# Open the video file for writing
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('video.mp4', fourcc, 25.0, (640, 480))

# Start recording video
while True:

    # Capture a frame from the Tello drone
    ret, frame = cap.read()

    # If the frame is empty, break out of the loop
    if not ret:
        break

    # Write the frame to the video file
    out.write(frame)

    # Press the Esc key to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the VideoCapture object
cap.release()

# Release the VideoWriter object
out.release()

# Disconnect from the Tello drone
drone.disconnect()

