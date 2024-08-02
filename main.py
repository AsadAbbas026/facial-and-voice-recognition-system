import pyttsx3
import wave
import numpy as np
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def record_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    return audio

def recognize_sentence(audio):
    recognizer = sr.Recognizer()

    try:
        print("Recognizing sentence...")
        sentence = recognizer.recognize_google(audio).lower()
       # print(f"Recognized sentence: {sentence}")
        return sentence

    except sr.UnknownValueError:
        print("Sorry, I could not understand the sentence.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def compare_with_stored_voice(detected_audio, stored_data, expected_sentence):
    detected_data = np.frombuffer(detected_audio.frame_data, dtype=np.int16)

    correlation = np.correlate(detected_data, stored_data, mode='full')

    threshold = 5000
    if np.max(correlation) > threshold:
        detected_sentence = recognize_sentence(detected_audio)
        if detected_sentence and detected_sentence == expected_sentence:
            speak("Accessing Facial Recognition. Please Wait")
            import FR  # Face Recognition Application
            return True
        else:
            print("Detected sentence does not match the expected sentence.")
            return False
    else:
        return False

def load_stored_voice(file_path):
    stored_audio = wave.open(file_path, 'rb')
    stored_data = np.frombuffer(stored_audio.readframes(stored_audio.getnframes()), dtype=np.int16)
    return stored_data

def record_and_save_voice(file_path):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(audio.frame_data)

if __name__ == "__main__":
    known_users = ["asad"]
    stored_audio_path = "stored_voice.wav"
    expected_sentence = "hey jarvis"  # Set the expected sentence

    # Uncomment the following line to record and save your voice (do this only once)
    # record_and_save_voice(stored_audio_path)

    stored_data = load_stored_voice(stored_audio_path)
    audio = record_audio()
    if compare_with_stored_voice(audio, stored_data, expected_sentence):
        command = input("Enter a command: ").lower()

        if command == "hey jarvis":
            print("Recognized command: Hey JARVIS!")
        elif command == "exit":
            print("Exiting the program.")
    else:
        print("Voice doesn't match the stored sample or the detected sentence doesn't match the expected sentence. Please repeat the command.")
