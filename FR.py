import cv2

import pyttsx3
print(cv2.__version__)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 2

names = ['', 'asad', 'abbas']

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

authorized_user_recognized = False  # Variable to track if the authorized user has been recognized

while not authorized_user_recognized:
    ret, img = cam.read()
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        converted_image,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])
        if 0 <= id < len(names) and names[id] == 'asad' and not authorized_user_recognized:
            name = 'asad'
            accuracy = "   {0}%".format(round(100 - accuracy))
            speak("Facial Recognition Successful")
            speak("Welcome, Asad Abbas")
            authorized_user_recognized = True  # Set the variable to True after recognizing the authorized user
        else:
            name = "unknown"
            accuracy = "   {0}%".format(round(100 - accuracy))

        cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(accuracy), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

# Subsequent commands can be executed here

#print("Thanks for using this program, have a good day")
cam.release()
cv2.destroyAllWindows()