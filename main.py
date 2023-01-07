'''
install SpeechRecognition, 
PyAudio (speech input), gtts, playsound, PyObjC packages
'''
import speech_recognition as sr
import webbrowser
import playsound
import os
import random
from gtts import gTTS
import time

#reading audio files
r = sr.Recognizer()

def record_audio(ask = False):
    #using microphones to speech input
    with sr.Microphone() as source:
        if ask:
            iris_speak(ask)
        r.adjust_for_ambient_noise(source)
        #detect audio from source
        audio = r.listen(source)
        voice_data = ''
        try:
            #using google web speech API
            voice_data = r.recognize_google(audio)
        #error handling
        except sr.UnknownValueError:
            iris_speak("Sorry, I didn't get that")
        except sr.RequestError:
            iris_speak("Sorry, My speech service is down")
        return voice_data

#assistant replies- text to speech
def iris_speak(audio_string):
    #initialize text to speech with audio input, english
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1,10000000)
    #naming audio file 
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    #playing audiofile
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

#assistant responses for various questions
def respond(voice_data):
    if 'what is your name' in voice_data:
        iris_speak('My name is Iris')
    if 'what is the time' in voice_data:
        iris_speak(time.ctime())
    
    #search for something on google search
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://www.google.com/search?q=' + search        
        webbrowser.get().open(url)
        iris_speak('Here is what i found for ' + search) #opens url

    #search for a location on google maps
    if 'find location' in voice_data:
        location = record_audio('What is the location you want to find?')
        url = 'https://www.google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        #prompt for location
        iris_speak('Here is the location of ' + location)

    #exit assistant
    if 'exit' in voice_data:
        exit()
        
time.sleep(1)

#prompt user/ assiatant greeting
iris_speak("How may I help you?")
#continue until user exits
while 1:
    voice_data = record_audio() 
    respond(voice_data)