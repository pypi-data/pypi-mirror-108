from Easy_AI import *

ai_m = initPyttsx3('voice')

def brain():
    while True:
        try:
            query = command.init().lower()
            if 'hello' in query:
                # speakGTTs('Hello', value="AI: ")
                ai_m.speak('Hello Boss', value="AI: ")
            elif 'moi' in query:
                ai_m.speak("Moi", value="AI: ")
        except KeyboardInterrupt:
            ai_m.speak('AI is quiting', value="AI: ")
            break
        except TypeError:
            print(" ")

brain()
