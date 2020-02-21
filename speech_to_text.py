# John Park
# Translates Speech to Text
import speech_recognition as rs # to work with Google speech-to-text API
import pyaudio                  # captures mic input
import audioop                  # to perform operations on audio
import os                       # to work with the operating system
import math                     # math operations
from os import system           # make the computer say stuff
import threading                # run multiple threads

# Microphone stream config
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 800  # int lower than THRESHOLD == silence

SILENCE_LIMIT = 1  # Silence limit in seconds. max ammount of seconds where
                   # only silence is recorded. When this time passes,
                   # recording finishes and file is delivered.
        
def audio_int(num_samples=50):
# Gets average audio intensity of mic sound
# avg = avg of 20% largest intensities recorded
    p = pyaudio.PyAudio()                   # get pyaudio obj
    stream = p.open(format=FORMAT,          # stream mic with previously defined configs
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
        for x in range(num_samples)] 
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print(" Average audio intensity is ", r)
    stream.close()
    p.terminate()
    if r > THRESHOLD: listen(0) # invokes listen func
    threading.Timer(SILENCE_LIMIT, audio_int).start()

def listen(x):
    r=rs.Recognizer()
    if x == 0:
        system('say Hi. How can I help?')
    with rs.Microphone() as source: audio = r.listen(source)
    try:
        print("here")
        text = r.recognize_google(audio)
        outputText = process(text.lower())
        return(outputText)
    except:
        if x == 1:
            system('say Good Bye!')
        else:
            system('say I did not get that. Please say again.')
            listen(1)

def process(text):
    print(text)
    return text

# main
audio_int()