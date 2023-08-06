from Easy_AI import *

def brain():
    while True:
        try:
            query = command.init().lower
            if 'hello' in query:
                speakGTTs('Hello', value="AI: ")
        except KeyboardInterrupt:
            speakGTTs('AI is quiting', value="AI: ")
            break

brain()
