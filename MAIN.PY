import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import pyttsx3
import wikipedia

source = r'C:\Users\Kiran\PycharmProjects\ALEXAPROJECT\chromedriver.exe'
service = Service(executable_path=source)
driver = webdriver.Chrome(service=service)

def say(answer):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('volume', 1.0)
    engine.say(answer)
    engine.runAndWait()

r = sr.Recognizer()
audio = None
text = None

def listen():
    global audio
    global text
    with sr.Microphone() as input:
        print("Listening")
        say("Listening")

        try:
            audio = r.listen(input, timeout=10, phrase_time_limit=15)
            text = r.recognize_google(audio).lower()
            print("Recognized text is", text)
            say(text)
            command()
        except:
            print("Listening timed out or did not recognize audio")
            say("Listening timed out or did not recognize audio")

def command():
    global text
    print("Inside process_command() function.")
    if text:
        if 'youtube' in text:
            youtube()
        elif 'wikipedia' in text:
            wikipedia()
        elif 'amazon' in text:
            amazon()
        else:
            print("No recognized command.")
            say("No recognized command.")
    else:
        print("Text is None or empty.")
        say("Text is None or empty.")

def youtube():
    global text
    print("YouTube command detected.")
    say("YouTube command detected.")
    listen()
    try:
        driver.get('https://www.youtube.com/')

        # Wait for the search box to be present
        ytsearch = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'search_query'))
        )
        print("YouTube search box located")
        say("YouTube search box located")

        # Input to the web
        ytsearch.send_keys(text)
        print("Text entered into search box:", text)
        say("Text entered into search box")
        ytsearch.send_keys(Keys.ENTER)
        print("Search executed")
        say("Search executed")
        # Discontinue the browser from exit, by calling listenexit()
        listenexit()
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start.")

def wikipedia():
    global text
    print("Wikipedia command detected.")
    say("Wikipedia command detected.")
    print("Give a question to Wikipedia")
    say("Give a question to Wikipedia")
    listen()
    try:
        answer_wiki = wikipedia.summary(text, 10)
        print(answer_wiki)
        say(answer_wiki)
        listenexit()
    except:
        print("There is a connection problem from WebDriver to Wikipedia")
        say("There is a connection problem from WebDriver to Wikipedia")

def amazon():
    global text
    print("Amazon command detected. Enter search item in Amazon")
    say("Amazon command detected. Enter search item in Amazon")
    listen()
    try:
        driver.get('https://www.amazon.com')
        amazonpath = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'twotabsearchtextbox'))
        )
        amazonpath.send_keys(text)
        amazonpath.send_keys(Keys.RETURN)
        listenexit()
    except Exception as e:
        print(f"Error accessing Amazon: {e}")
        say("Error accessing Amazon")

def listenexit():
    global audio
    global text
    with sr.Microphone() as source:
        print("Listening")
        say("Listening")
        say("Say exit to exit or new tab to continue")
        while True:
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=15)
                print("Audio captured")
                say("Audio captured")
                text = r.recognize_google(audio).lower()
                print("You said:", text)
                say(text)
                if 'exit' in text:
                    print("Exit command received.")
                    say("Exit command received")
                    driver.quit()  # Exit entire web browser
                    break
                if 'new tab' in text:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    listen()
            except Exception as e:
                print(f"Audio not recognizable or ensure there is no background sound and microphone worked properly. Error: {e}")
                say("Audio not recognizable or ensure there is no background sound and microphone worked properly")

listen()




