from Easy_AI import *

ai_m = initGTTs(value='AI: ')

try:
    def brain():
        while True:
            try:
                query = command.init().lower()
                if 'hello' in query:
                    ai_m.say('Hello')
                elif 'stop' in query:
                    ai_m.say('Ok')
                    break
                else:
                    ai_m.say("Bye")
                    break
            except KeyboardInterrupt:
                ai_m.say('Bye')
                break
except FileNotFoundError:
    os.system('mkdir cache')