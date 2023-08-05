import pyttsx3
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

def speak(audio, voiceid = 1,rate = 150, volume = 0.8):
    engine.setProperty('voice',voices[voiceid].id)
    engine.setProperty('rate',rate)
    engine.setProperty('volume',volume)
    engine.say(audio)
    engine.runAndWait()
