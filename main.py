import webbrowser
import speech_recognition as sr
import pyttsx3
import musiclib
import feedparser
from openai import OpenAI

# object creation
recognizer=sr.Recognizer()
engine=pyttsx3.init() 
new_api= "API KEY HERE"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="API KEY HERE"
)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def read_google_news():
    feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
    for entry in feed.entries[:5]:
        engine.say(str(entry.title))

def aiProcess(user_input):
    try:
        completion = client.chat.completions.create(
            model="google/gemma-3n-e2b-it:free",

            messages=[{"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud."
            " Give short responses please"},
            {"role": "user", "content": user_input}

    ]
    )

        reply = completion.choices[0].message.content
        print("Jarvis:", reply)
        engine.say(reply)
        
    except Exception as e:
        print("Error talking to AI:", e)
        engine.say("Sorry, I could not connect to the AI.")

           

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclib.music[song]
        webbrowser.open(link)
    
    elif "news today" in c.lower():
        read_google_news()

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 

if __name__=="__main__":
    speak("Hello I am Jarvis your Assistant !")
    
    while True:
        r= sr.Recognizer()

        try:
            # obtain audio from the microphone and recognize speech using Google 
            with sr.Microphone() as source:
                print("Say Jarvis to Activate:-")
                audio = r.listen(source,timeout=1)

            word=r.recognize_google(audio)

            if word.lower()=="exit":
                print("SHUTDOWN")
                break

            # Listen for the wake word "Jarvis"
            elif word.lower()=="jarvis":
                with sr.Microphone() as source:
                    engine.say("Jarvis Activated")
                    audio = r.listen(source,timeout=5)

                command=r.recognize_google(audio)
                print("You said:- ",command)
                processCommand(command)

        except Exception as e:

            print("Error; {}".format(e))

