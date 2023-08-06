import pyttsx3
import speech_recognition as sr
import playsound
import random
import os
from gtts import gTTS



class initGTTs:
    def __init__(self, lang_='en', value=''):







        """ Not Recommend
        @param lang_: Choose a language to say default is en == English
        - Vie: Phải Tạo Thư Mục cache Trước Khi Sài Hàm speakGTTs().
        - Eng: Must Create Folder cache Before Using speakGTTs() Function.
        """




        self.lang_ = lang_



        self.value = value



    def say(self, text):
        """
        Function say() Of Class initGTTs Will Say Data String Of text Parameter
        """
        self.r1 = random.randint(1, 900000)



        self.r2 = random.randint(1, 900000)



        self.tts = gTTS(text, lang=self.lang_)



        self.filename = 'cache\\voice ' + str(self.r1) + 'randomText' + str(self.r2) +".mp3"



        self.tts.save(self.filename)



        print(self.value + text)



        playsound.playsound(self.filename)



        os.remove(self.filename)
    




class initPyttsx3:



    def __init__(self, name, voice='en-f', value=''):





        """Recommend

        Support Voice:
            System Voice:

            - en = English: TTS_MS_EN-US_DAVID_11.0
            - en-f = English Female: TTS_MS_EN-US_ZIRA_11.0

            Must Installing Voice:

            - vi = Vietnamese: MSTTS_V110_viVN_An. Link video install https://www.youtube.com/watch?v=qVMHoCtjLag
            - vi-f = Vietnamese Female: VE_Vietnamese_Linh_22kHz. Link video install https://www.youtube.com/watch?v=Uy2aNbrj7PM
        """



        self.value = value



        self.ai = pyttsx3.init()



        self.voices = self.ai.getProperty('voices')



        if voice == 'vi-f':
            self.vi_f_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\VE_Vietnamese_Linh_22kHz"
            self.ai.setProperty(name, self.vi_f_voice)



        elif voice == 'vi':
            self.vi_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
            self.ai.setProperty(name, self.vi_voice)



        elif voice == 'en-f':
            self.en_f_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
            self.ai.setProperty(name, self.en_f_voice)



        elif voice == 'en':
            self.en_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
            self.ai.setProperty(name, self.en_voice)




    def say(self, audio):





        """
        Function say() Of Class initPyttsx3 Will Say Data String Of audio Parameter
        """



        print(self.value + audio)



        self.ai.say(audio)



        self.ai.runAndWait()
        

class command:



    @staticmethod



    def init(lang='en', value=''):





        """
        Function init() Of Class command Is A Recognizer Function.
        This Function Will Use Microphone To Recognize
        """





        c = sr.Recognizer()



        with sr.Microphone() as source:



            c.pause_threshold = 1



            audio = c.listen(source)



            try:



                query = c.recognize_google(audio, language=lang)



                print(value + query)





            except sr.UnknownValueError:



                print('Error Code: UnknownValueError')



                query = str(input("Your order is: "))



            return query

