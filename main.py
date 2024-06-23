#import libraries
import datetime
from ultralytics import YOLO
import cv2
import pyttsx3
import easyocr
import speech_recognition as sr
from difflib import get_close_matches
import os
import sounddevice as sd

#load the models into memory
#Optical Character Recognition model
reader = easyocr.Reader(['ch_sim','en'])
#object detection model
model = YOLO("yolo-Weights/yolov8x.pt")


#make USB Audio Device as default device
devs = sd.query_devices()
defin = 8417
defout = 7346
while True:
    try:
        for dev in devs:
            if 'USB Audio Device' in dev['name']:
                defout = dev['index']
            if 'USB Audio Device' in dev['name']:
                defin = dev['index']
            sd.default.device = [defin, defout]
        if defin < 100 and defout < 100:
            break
    except:
        pass

#using Recognizer class to initialize speech recognition
rr = sr.Recognizer()
#set energy_threshold to avoid noise
rr.energy_threshold = 5000  

#mic function to record voice and convert it to text
def mic():
    with sr.Microphone() as source:
        audio_text = rr.listen(source, 4, 4)
        try:
            speak(' i heard you please wait ')
            text = rr.recognize_whisper(audio_text, language="english",model='tiny.en')
            
            return text
        except:
            text = "sorry i didnt hear you"
            return text

#closeMatches is a function selects the correct command provided by the user by comparing the user's sentence with the available list of commands.
def closeMatches(word):
    patterns = ["what is in front of me", "what time is it", "find the object", "restart the system", "what is the color",
                "read the words","shutdown"]
    matches: list = get_close_matches(word, patterns, n=1, cutoff=0.6)
    return matches[0] if matches else ""


#object names (using in YOLO model and closetracking)
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush", "i found it", "yes i found it"
              ]

#This function functions as a 'closeMatches' function, but we use it in the case of find the object
def closetracking(word):
    tracking: list = get_close_matches(word, classNames, n=1, cutoff=0.6)
    return tracking[0] if tracking else "sorry i didnt hear you"

#using init class to initialize pyttsx3 (Text-to-speech library)
engine = pyttsx3.init()
#set rate of speak 120 to speak slowly
engine.setProperty('rate', 120)

#The 'speak' function converts any text into speech
def speak(sentence):
    sp = engine.say(sentence)
    engine.runAndWait()
    return sp

#Give instructions to the user
speak("Hello, please listen to this information , You can ask about the objects in front of you by saying , 'What is in front of me?' or inquire about the time by saying , 'What time is it?' To know the color of an object , say , 'What is the color?' If you want to read any word in front of you , simply say , 'Read the words' For tracking any object , say 'Find the object' To restart the system , say 'Restart the system,' and for shutting down the system , say 'Shutdown' , Now , how can I help you?")
while True:
    #We use 'try' to ensure the code doesn't stop in case of any error
    try:
        #Take the command from the user through the 'mic' function
        command = mic()
        #Comparing the user's speech with the commands listed in 'closeMatches' and selecting the appropriate command from them
        tt = closeMatches(command)
        #If the user says 'what is in front of me' this condition will be executed
        if tt.lower() == "what is in front of me":
            #open the camera
            cap = cv2.VideoCapture(0)
            #take a picture from the camera
            success, img = cap.read()
            #put the picture in YOLO model to detect the objects
            results = model(img, stream=True)
            #release software resource and hardware resource.
            cap.release()
            #for loop to tell the user what is the objects infront of him
            for r in results:
                boxes = r.boxes

                for box in boxes:
                    cls = int(box.cls[0])
                    speak(classNames[cls])
            speak("done , how can i help you")

        elif tt.lower() == "what time is it":
            Time = datetime.datetime.now().strftime("%I:%M %p")
            speak(Time)

        # If the user says 'read the words' this condition will be executed
        elif tt.lower() == "read the words":
            cap = cv2.VideoCapture(0)
            _, image = cap.read()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #convert from BGR2GRAY
            cap.release()
            #using readtext to read any word in the image
            result = reader.readtext(image, detail = 0)
            speak(result)
            speak('done,how can i help you')

        # If the user says 'what is the color' this condition will be executed
        elif tt.lower() == "what is the color":
            cap = cv2.VideoCapture(0)
            _, frame = cap.read()
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert from BGR2HSV
            cap.release()
            height, width, _ = frame.shape #get dimensions from the image
            cx = int(width / 2) #cetner of x axis
            cy = int(height / 2) #cetner of y axis

            pixel_center = hsv_frame[cy, cx]
            hue_value = pixel_center[0] #hue_value (value of the color)
            color = "Undefined"
            if hue_value < 1:
                color = "BLACK"
                speak("BLACK")
            elif hue_value < 5:
                color = "RED"
                speak("RED")
            elif hue_value < 22:
                color = "ORANGE"
                speak("ORANGE")
            elif hue_value < 33:
                color = "YELLOW"
                speak("YELLOW")
            elif hue_value < 78:
                color = "GREEN"
                speak("GREEN")
            elif hue_value < 131:
                color = "BLUE"
                speak("BLUE")
            elif hue_value < 170:
                color = "VIOLET"
                speak("VIOLET")
            else:
                color = "RED"
                speak("RED")
            speak('done , how can i help you')

        #If the user says 'restart the system' this condition will be executed
        elif tt.lower() == "restart the system":
            speak("system is restarting now")
            #restart the system
            os.system("sudo reboot")

        #If the user says 'shutdown' this condition will be executed
        elif tt.lower() == "shutdown":
            speak("ok goodbye")
            #Shutdown the system
            os.system("sudo shutdown now")

        #If the user says 'find the object' this condition will be executed
        elif tt.lower() == "find the object":
        #This if statement will help you find any object you want and navigate to it
            speak("What is the object")
            objec = mic()
        #Compare the user's speech with the objects listed in 'closetracking' and select the appropriate object from them
            objectt = closetracking(objec.lower())
        #If the object is in the 'classNames,' this condition will be executed
            if objectt in classNames:
                speak("ok lets find it")
                cont = 0 #for counting how many times the loop has been repeated and every 5 times, the user is asked if they found it or not
                anss = ""
                while True:
                    cont = cont + 1
                    cap = cv2.VideoCapture(0)
                    success, img = cap.read()
                    results = model(img, stream=True)
                    cap.release()

                    for r in results:
                        boxes = r.boxes

                        for box in boxes:
                            cls = int(box.cls[0])
                            if objectt in classNames[cls]:
                                speak("it is in your view")
                    #Here, the user is asked whether they found it or not
                    if cont in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
                        speak("Did you found it")
                        ansss: str = mic()
                        anss: str = closetracking(ansss)
                    #If the user says 'yes I found it,' break the while loop otherwise, continue
                    if anss.lower() == "yes i found it" or anss.lower() == "i found it":
                        speak('ok how can i help you')
                        break
            #If the object is not in the 'classNames,' this condition will be executed
            elif objectt != classNames or objec == 'sorry i didnt hear you':
                speak("Sorry i dont know what is that")
            else:
                speak("Sorry i dont know what is that")
        #If the user said an incorrect command
        else:
            speak("try again")
    #If any error occurs in the code
    except:
        pass
