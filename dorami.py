import speech_recognition as sr
import webbrowser
import wikipedia
import datetime
import os
import pywhatkit
import edge_tts
import asyncio
from playsound import playsound
import uuid
import re

# -------- SETTINGS --------
ASSISTANT_NAME = "Dorami"
PASSWORD = "1234"

recognizer = sr.Recognizer()

# 🔥 REAL-TIME TUNING
recognizer.pause_threshold = 1.2
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

# -------- CALIBRATE ONCE --------
with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

# -------- SPEAK --------
async def _speak_async(text):
    filename = f"voice_{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-IN-NeerjaNeural"
    )

    await communicate.save(filename)
    playsound(filename)

    try:
        os.remove(filename)
    except:
        pass

def speak(text):
    print(f"{ASSISTANT_NAME}: {text}")
    asyncio.run(_speak_async(text))

# -------- FAST LISTEN --------
def listen():
    with sr.Microphone() as source:
        print("Listening...")

        audio = recognizer.listen(
            source,
            timeout=None,
            phrase_time_limit=6
        )

    try:
        command = recognizer.recognize_google(audio, language="en-IN")
        print("You:", command)
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Network error")
        return ""

# -------- AUTH --------
def authenticate():
    speak("Please say the password")
    while True:
        command = listen()
        if command:
            if PASSWORD in command:
                speak("Access granted")
                return True
            else:
                speak("Wrong password, try again")

# -------- TIME --------
def tell_time():
    now = datetime.datetime.now()
    speak(f"The time is {now.strftime('%H:%M')}")
    speak(f"Today's date is {now.strftime('%d %B %Y')}")

# -------- CALCULATOR --------
def calculate(command):
    try:
        expression = command.replace("dorami", "").replace("calculate", "")

        expression = expression.replace("plus", "+")
        expression = expression.replace("minus", "-")
        expression = expression.replace("into", "*")
        expression = expression.replace("multiplied by", "*")
        expression = expression.replace("x", "*")
        expression = expression.replace("divided by", "/")

        expression = re.sub(r"[a-zA-Z]", "", expression)

        result = eval(expression)

        os.system("calc")
        speak(f"The answer is {result}")

    except:
        speak("Sorry, I could not calculate that")

# -------- YOUTUBE --------
def play_youtube(command):
    song = command.replace("play", "").replace("on youtube", "").strip()
    speak(f"Playing {song} on YouTube")
    pywhatkit.playonyt(song)

# -------- SPOTIFY --------
def open_spotify(command):
    song = command.replace("play", "").replace("on spotify", "").strip()
    speak(f"Playing {song} on Spotify")
    webbrowser.open(f"https://open.spotify.com/search/{song}")

# -------- SEARCH --------
def smart_search(command):
    query = command.replace("dorami", "")
    query = query.replace("look up", "").replace("search about", "").replace("search", "").strip()

    speak(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("Opened Google for more details")

# -------- APPS --------
def open_apps(command):
    if "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("calc")
    elif "chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

# -------- WEBSITES --------
def open_sites(command):
    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")
    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

# -------- COMMAND ENGINE --------
def process_command(command):

    if "dorami stop" in command:
        speak("Shutting down")
        exit()

    elif "calculate" in command:
        calculate(command)

    elif "hello" in command:
        speak("Hello, how can I help you")

    elif "time" in command or "date" in command:
        tell_time()

    elif "play" in command and "spotify" in command:
        open_spotify(command)

    elif "play" in command:
        play_youtube(command)

    elif "look up" in command or "search" in command:
        smart_search(command)

    elif "open" in command:
        open_apps(command)
        open_sites(command)

    elif "wikipedia" in command:
        try:
            topic = command.replace("wikipedia", "").strip()
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except:
            speak("No results found")

# -------- MAIN --------
speak("Dorami starting")

if authenticate():
    speak("I am ready")

    while True:
        command = listen()

        if command:
            process_command(command)