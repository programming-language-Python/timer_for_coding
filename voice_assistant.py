import pyttsx3

speak_engine = pyttsx3.init()


def speak(text_to_say):
    speak_engine.say(text_to_say)
    speak_engine.runAndWait()
    speak_engine.stop()
