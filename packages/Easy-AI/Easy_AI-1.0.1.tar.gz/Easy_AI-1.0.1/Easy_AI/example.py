from Easy_AI import *
import datetime
import webbrowser as wb


ai_m = initPyttsx3('voice', value='AI: ')

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    ai_m.say(Time)

def welcome():
    hour = datetime.datetime.now().hour
    
    if hour >= 6 and hour < 12:
       ai_m.say("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
       ai_m.say("Good Afternoon Sir!")
    elif hour >= 18 and hour < 24:
       ai_m.say("Good Evening Sir!")
    ai_m.say("How Can I Help You")


def brain():
    while True:
        # welcome()
        try:
            query = command.init(value='Khoa: ').lower()
            if 'hello' in query:
                ai_m.say("Hello Sir!")
            elif query == 'What Time Is It':
                time()
            elif 'search' in query:
                search = command.init(value='Search: ')
                print('Searching . . .')
                try: 
                    ai_m.say('Searching Successfully')
                    wb.open(f'https://www.google.com/search?q={search}', 0)
                except:
                    ai_m.say('Searching Failed')
            elif 'Stop' in query:
                ai_m.say('AI Is Quiting Good Bye Sir!')
                break
        except KeyboardInterrupt:
            ai_m.say('AI Is Quiting Good Bye Sir!')
            break

brain()
