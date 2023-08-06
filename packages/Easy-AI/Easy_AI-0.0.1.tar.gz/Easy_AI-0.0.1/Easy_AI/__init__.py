import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import playsound

def speakGTTs(text, lang_='en', **kwargs):
        text = text
        tts = gTTS(text, lang=lang_)
        filename = 'voice.mp3'
        tts.save(filename)
        print(kwargs['value'] + text)
        playsound.playsound(filename)
    


class initPyttsx3:
    def __init__(self, name, voiceId: int = 1):
        self.ai = pyttsx3.init()
        self.voice = self.ai.getProperty('voices')
        self.ai.setProperty(name, self.voice[voiceId].id)
    def speak(self, audio, **kwargs):
        print(kwargs['value'] + audio)
        self.ai.say(audio)
        self.ai.runAndWait()
        return audio

class command:
    @staticmethod
    def init(lang='en'):
        c = sr.Recognizer()
        with sr.Microphone() as source:
            c.pause_threshold = 1
            audio = c.listen(source)
            try:
                query = c.recognize_google(audio, language=lang)
                print(f"Khoa: {query}")
            except sr.UnknownValueError:
                print('Error Code: UnknownValueError')
                query = str(input("Your order is: "))
            return query

