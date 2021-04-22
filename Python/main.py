import os
import struct
import sys
import time
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from gtts import gTTS
import http.client
import http.server
import http
import json
import requests
import commands
import spotifyCode
import webbrowser

#Spotify activation
ready = False

spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
SpotifyToken = spotifyResult[0]
SpotifyDeviceID = spotifyResult[1]
ready = spotifyResult[2]

#json variables
with open('settings.json', 'r') as myfile:
  data = myfile.read()

obj = json.loads(data)

DiscordToken = str(obj['TOKEN'])
gid = str(obj['gid'])
uid = str(obj['uid'])

# allows to run this script on windows
if not os.name == "nt":
  from pixel_ring import pixel_ring
  from gpiozero import LED

  power = LED(5)
  power.on()
  pixel_ring.set_brightness(10)

wakeword = ["raspberry ", "rsp ", "hairspray ", "harrislee ", "restaurant "]

while(ready == True):
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
    print("Say something!")
    print()
    audio = r.listen(source)

  try:
    Text = r.recognize_google(audio, language='de-DE')
    Text = Text.lower()
    print(Text)

    for x in wakeword:
      if x + "was geht" in Text:
        SpeechText = commands.was_geht()
      elif "danke" in Text:
        SpeechText = commands.danke()
      elif "ich bin so gut" in Text:
        SpeechText = commands.gut()
      elif x + "uhrzeit" in Text or x + "wie viel uhr ist es gerade" in Text or x + "wie spät ist es" in Text:
        SpeechText = commands.uhrzeit(time)
      elif x + "datum" in Text:
        SpeechText = commands.datum(time)
      elif x + "mach einen backflip" in Text:
        SpeechText = commands.backflip()
      elif x + "lösch mich" in Text or x + "flash mich" in Text or x + "fick mich" in Text or x + "rette mich" in Text:
        SpeechText = commands.disconnect_discord(http, json, DiscordToken, gid, uid)
      elif x + "pausiere meine musik" in Text:
        try:
          SpeechText = commands.spotify_pause(SpotifyToken, SpotifyDeviceID, requests)
        except:
          spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
          SpotifyToken = spotifyResult[0]
          SpotifyDeviceID = spotifyResult[1]
          ready = spotifyResult[2]
      elif x + "setze meine musik fort" in Text or x + "setze musik fort" in Text or x + "setze meine musik vor" in Text or x + "meine musik fort" in Text:
        try:
          SpeechText = commands.spotify_play(SpotifyToken, SpotifyDeviceID, requests)
        except:
          spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
          SpotifyToken = spotifyResult[0]
          SpotifyDeviceID = spotifyResult[1]
          ready = spotifyResult[2]
      elif x + "überspringe diesen song" in Text or x + "überspringe den track" in Text or x + "überspringen track" in Text or x + "überspring den dreck" in Text or x + "überspringe den dreck" in Text or x + "überspringen dreck" in Text:
        try:
          SpeechText = commands.spotify_skip(SpotifyToken, SpotifyDeviceID, requests)
        except:
          spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
          SpotifyToken = spotifyResult[0]
          SpotifyDeviceID = spotifyResult[1]
          ready = spotifyResult[2]
      elif x + "fick dich" in Text:
        SpeechText = "Ha hahaha aha ha"
      elif x + "verpissdich" in Text:
        speak("O O O O O O O O O")
        exit()
      elif x in Text:
        SpeechText = commands.error()
      else:
        pass

  except sr.UnknownValueError:
    print("Ich konnte dich nicht verstehen!")
  except sr.RequestError:
    pass

  try:
    if SpeechText != "":
      if not os.name == "nt":
        pixel_ring.think()

      speak(SpeechText)

      if not os.name == "nt":
        pixel_ring.off()
  except Exception as e:
    print("Error")

power.off()