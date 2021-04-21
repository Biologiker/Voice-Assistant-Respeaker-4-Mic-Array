import os
import struct
import sys
import time
import datetime
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from gtts import gTTS
from pixel_ring import pixel_ring
from gpiozero import LED
import http.client
import json

#spotify_client = SpotifyClient(os.getenv('SPOTIFY_TOKEN'))
# lol

power = LED(5)
power.on()
pixel_ring.set_brightness(10)

wakeword = ["raspberry ", "rsp ", "hairspray ", "harrislee ", "restaurant "]
gid = ["751734515420102737", "734082661143805973"]

while(True):
    Text = ""
    SpeechText = ""

    def speak(text):
        tts = gTTS(text=text, lang="de")
        filename = "voice.mp3"
        tts.save(filename)

        song = AudioSegment.from_mp3(filename)
        play(song)

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print()
        print("Say something!")
        audio = r.listen(source)

    try:
        Text = r.recognize_google(audio, language='de-DE')
        Text = Text.lower()
        print(Text)

        for x in wakeword:
            if x + "was geht" in Text:
                SpeechText = "Ich mag dich nicht"
            elif x + "uhrzeit" in Text or x + "wie viel uhr ist es gerade" in Text or x + "wie spät ist es" in Text:
                SpeechText = "Es ist " + \
                    time.strftime('%H:%M:%S', time.localtime())
            elif x + "datum" in Text:
                SpeechText = "Heute ist der " + \
                    time.strftime('%Y-%m-%d', time.localtime())
            elif x + "mach einen backflip" in Text:
                SpeechText = "Wuuu Backflip"
            elif x + "verpissdich" in Text:
                exit()
            elif x + "lösch mich" in Text:
                for y in gid:
                    print("löschen")
                    conn = http.client.HTTPSConnection("discordapp.com")
                    payload = json.dumps({
                        "channel_id": None
                    })
                    headers = {
                        'Authorization': 'mfa.4VcfC3QC9SJ1ihXjCMH7sqf4qFspq9nDm3uq2U1MkVxaIgOfHY5eh16Y50OaC5ufzCeYFufpHjpEeK3gRFtK',
                        'Content-Type': 'application/json',
                    }
                    conn.request("PATCH", "/api/v6/guilds/" + y +
                                 "/members/454315560503738400", payload, headers)
                    res = conn.getresponse()
                    data = res.read()
                    print(data.decode("utf-8"))
            else:
                pass

    except sr.UnknownValueError:
        print("Ich konnte dich nicht verstehen!")
    except sr.RequestError:
        pass

    try:
        if SpeechText != "":
            pixel_ring.wakeup()
            speak(SpeechText)
            pixel_ring.off()
    except Exception as e:
        print("Error")

power.off()
