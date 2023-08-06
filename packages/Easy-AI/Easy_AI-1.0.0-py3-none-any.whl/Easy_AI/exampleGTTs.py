from Easy_AI import *

try:
    def brain():
        while True:
            try:
                query = command.init().lower()
                if 'Hello' in query:
                    speakGTTs('Hello', value="")
                elif 'stop' in query:
                    speakGTTs('Ok', value="")
                    break
                else:
                    speakGTTs("Bye", value="")
                    break
            except KeyboardInterrupt:
                speakGTTs('Bye', value="")
except FileNotFoundError:
    os.system('mkdir cache')