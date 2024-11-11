import speech_recognition as aa
import pyttsx3
import sys
from urllib.request import urlopen
import pyjokes
import json
import time
import cv2
import pytesseract
from transformers import pipeline
from transformers import MarianMTModel, MarianTokenizer
import torch
import tellopy

listener = aa.Recognizer()

machine = pyttsx3.init()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
cap = cv2.VideoCapture(0)

drone = tellopy.Tello()

drone.connect()

language = "fr"

def talk(text):
    machine.say(text)
    machine.runAndWait()

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
         if "pale" in instruction:
             instruction = instruction.replace('pale', '')
             print(instruction)


    except aa.UnknownValueError:
             print("Sorry could you please try again?")

    return instruction

def translate_text(input_text, source_lang, target_lang, max_length=50):
    # Load pre-trained MarianMT model and tokenizer
    model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    # Tokenize the input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Perform translation
    with torch.no_grad():
        translated_ids = model.generate(input_ids, max_length=max_length)
    
    # Decode the translated text
    translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True, max_length=max_length)
    return translated_text

def take_command():
    r = aa.Recognizer()
    with aa.Microphone() as source:
        r.pause_threshold = 0.5
        r.energy_threshold= 300

def play_Pale():
    instruction = input_instruction()
    print(instruction)
    if 'location details' in instruction:
         url = 'http://ipinfo.io/json'
         response = urlopen(url)
         data = json.load(response)
         print(data)
         talk(data)

    elif "timer for" in instruction:
         huma = instruction.replace('timer for', " ")
         my_time = int(huma)

         for x in range(my_time, 0, -1):
            seconds = x % 60
            minutes = int(x / 60) % 60
            hours = int(x / 3600) % 24
            print(f"{hours:02}:{minutes:02}:{seconds:02}")
            time.sleep(1)
            time.sleep(3)

         print_and_talk("Time's Up Sir!")

    elif "detect text" in instruction:
        while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150, apertureSize=3)
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) > 100:
                        x, y, w, h = cv2.boundingRect(contour)
                        text_region = frame[y:y+h, x:x+w]
                        
                        
                        text = pytesseract.image_to_string(text_region)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                cv2.imshow('Live Text Detection', frame)
                
                # Exit the loop when 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                print(text)
        cap.release()
        cv2.destroyAllWindows()

    elif "translate text" in instruction:
        while True:
                # Capture a frame from the camera
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Convert the frame to grayscale for better text detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Perform text detection using an edge detection method (Canny)
                edges = cv2.Canny(gray, 50, 150, apertureSize=3)
                
                # Find contours in the edge-detected image
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    # Filter out small contours
                    if cv2.contourArea(contour) > 100:
                        x, y, w, h = cv2.boundingRect(contour)
                        text_region = frame[y:y+h, x:x+w]
                        
                        # Perform OCR on the text region using Tesseract
                        text = pytesseract.image_to_string(text_region)
                        
                        # Draw a bounding box around the detected text region
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        # Display the recognized text
                        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                cv2.imshow('Live Text Detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                print("Original Text: " + text)
                input_text = text
                source_lang = "fr" 
                target_lang = "en"

                translated_text = translate_text(input_text, source_lang, target_lang, max_length=100)
                print_and_talk("Translated:", translated_text)
                cap.release()
                cv2.destroyAllWindows()
    
    elif "nothing" in instruction or "abort" in instruction or "stop" in instruction:
        talk("okay")
        talk("Bye Sir, have a good day.")
        sys.exit()

    else:
        talk("I don't understand sir!")
    
play_Pale()