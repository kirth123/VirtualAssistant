import pyttsx3
import speech_recognition as sr
import webbrowser 
import datetime 
import wikipedia
import json
import requests

name = ''
vol = 0
rate = 0
gender = 0

def takeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 1.0
        audio = r.listen(source)
         
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='en-in')
            print("the command is printed=", Query)
             
        except Exception as e:
            print(e)
            print("Can you say that again")
            return "None"
         
        return Query
 
def speak(audio):
     
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[gender].id) # [0]=male voice and [1]=female voice in set Property.
    engine.setProperty('voice', rate) #default rate is 200
    engine.setProperty('volume', vol)
    engine.say(audio) 
    engine.runAndWait()
 
def tellDay():
     
    day = datetime.datetime.today().weekday()
    Day_dict = {0: 'Monday', 1: 'Tuesday',
                2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday',
                6: 'Sunday'}
     
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)
 
 
def tellTime():
    time = str(datetime.datetime.now())
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speak("The time is " + hour + " Hours and " + min + " Minutes")   
 
def Hello():
    global name
    global gender
    global vol
    global rate

    name = input('What do you want the name of the AI to be?\n')
    gender = int(input('What gender do you want the AI to be? (0 for male, 1 for female)\n'))
    vol = float(input('How loud do you want the AI to talk?\n'))
    rate = int(input('How fast do you want the AI to talk? (default is 200)\n'))
    speak(f"Hello, I am your desktop assistant, {name}. How can I help you today?")

def Take_query():
    Hello()
     
    while(True): 
        query = takeCommand().lower()

        if "open" in query:
            start = query.index('open') + 5
            speak("Opening " + query[5:])
            webbrowser.open("https://www.google.com/search?q=" + query[5:])
            continue

        elif "+" in query:
            query = query.replace(',', '')
            op = query.index('+')
            first = int(query[:op-1])
            second = int(query[op+2:])
            sum = str(first + second)
            speak(str(first) + " plus " + str(second) + " is " + sum)
            print(sum)

        elif "-" in query:
            query = query.replace(',', '')
            op = query.index('-')
            first = int(query[:op-1])
            second = int(query[op+2:])
            sum = str(first - second)
            speak(str(first) + " minus " + str(second) + " is " + sum)
            print(sum)

        elif "*" in query:
            query = query.replace(',', '')
            op = query.index('*')
            first = int(query[:op-1])
            second = int(query[op+2:])
            sum = str(first * second)
            speak(str(first) + " times " + str(second) + " is " + sum)
            print(sum)

        elif "/" in query:
            query = query.replace(',', '')
            op = query.index('/')
            first = int(query[:op-1])
            second = int(query[op+2:])
            sum = str(first / second)
            speak(str(first) + " divided by " + str(second) + " is " + sum)
            print(sum)

        elif "what day is it" in query:
            tellDay()
        
        elif "what time is it" in query:
            tellTime()

        elif "bye" in query:
            speak("Goodbye! Have a good one!")
            exit()

        elif "news" in query:
            query_params = {
                    "source": "cnn",
                    "sortBy": "relevance",
                    "apiKey": "c9445449ee9a473d8744b362e56c821c"
            }
            main_url = "https://newsapi.org/v1/articles"
            res = requests.get(main_url, params=query_params)
            open_page = res.json()
            article = open_page["articles"]
            results = []
     
            for ar in article:
                results.append(ar["title"])
         
            for i in range(len(results)):
                print(results[i])
                speak(results[i])
            
        elif "from wikipedia" in query:
             
            speak("Checking the wikipedia ")
            query = query.replace("wikipedia", "")
             
            result = wikipedia.summary(query, sentences=4)
            speak("According to wikipedia")
            speak(result)
         
        elif "your name" in query:
            speak(f"My name is {name}")
 
if __name__ == '__main__':
     
    Take_query()