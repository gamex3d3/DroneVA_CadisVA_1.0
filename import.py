import tellopy
import cv2
import numpy as np

class PersonTracker:
    def __init__(self):
        self.tracker = cv2.TrackerKCF_create()
        self.bbox = None

    def update(self, frame):
        if self.bbox is not None:
            success, self.bbox = self.tracker.update(frame)
            return success
        else:
            return False

class TelloFollower:
    def __init__(self, drone):
        self.drone = drone
        self.person_tracker = PersonTracker()

    def follow_person(self):
        while True:
            # Capture a frame from the Tello drone
            ret, frame = self.drone.get_video_stream().read()

            # If the frame is empty, break out of the loop
            if not ret:
                break

            # Update the person tracker
            success = self.person_tracker.update(frame)

            # If the person tracker was successful, move the drone towards the person
            if success:
                # Get the person's bounding box
                bbox = self.person_tracker.bbox

                # Calculate the center of the person's bounding box
                center_x = (bbox[0] + bbox[2]) / 2
                center_y = (bbox[1] + bbox[3]) / 2

                # Move the drone towards the person
                self.drone.move(0, center_x - 320, center_y - 240, 0)

            # Press the Esc key to quit
            if cv2.waitKey(1) & 0xFF == 27:
                break

def main():
    # Connect to the Tello drone
    drone = tellopy.Tello()
    drone.connect()

    # Create a Tello follower object
    tello_follower = TelloFollower(drone)

    # Start following the person
    tello_follower.follow_person()

    # Disconnect from the Tello drone
    drone.quit()

if __name__ == "__main__":
    main()
