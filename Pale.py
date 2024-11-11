import speech_recognition as aa
import pyttsx3
import cv2
from urllib.request import urlopen
import json
import time
import tellopy
import numpy as np

listener = aa.Recognizer()

machine = pyttsx3.init()

drone = tellopy.Tello()
drone.connect()

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

def talk(text):
    machine.say(text)
    machine.runAndWait()

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

def print_and_talk(text):
    print(text)
    talk(text)

def input_instruction():
    global instruction
    try:   
        with aa.Microphone() as origin:
         print_and_talk("Listening sir...")
         speech = listener.listen(origin)
         instruction = listener.recognize_google(speech)
         instruction = instruction.lower()
         if "cadis" in instruction:
             instruction = instruction.replace('cadis', '')
             print(instruction)


    except aa.UnknownValueError:
             print("Sorry could you please try again?")

    return instruction

def take_command():
    r = aa.Recognizer()
    with aa.Microphone() as source:
        r.pause_threshold = 0.5
        r.energy_threshold= 300

def play_Pale():
    instruction = input_instruction()
    print(instruction)
    if 'location' in instruction:
         url = 'http://ipinfo.io/json'
         response = urlopen(url)
         data = json.load(response)
         print(data)
         talk(data)

    elif "picture" in instruction or "photo" in instruction:
        talk("taking a picture sir")
        drone.take_picture()

    elif "take off" in instruction or "fly" in instruction:
        talk("Ok! Taking off")
        drone.takeoff()

    elif "land" in instruction:
        talk("Landing sir!!")
        drone.land()

    elif "auto pilot" in instruction or "follow me" in instruction:
        tello_follower = TelloFollower(drone)
        tello_follower.follow_person()

    elif "disconnect" in instruction or "abort" in instruction or "stop" in instruction:
        talk("okay")
        talk("Bye Sir, have a good day.")
        drone.quit()

    else:
        talk("I don't understand sir!")
    
play_Pale()