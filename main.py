import os
import struct
import sys
import time
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from gtts import gTTS
import http.client
import json
import requests

with open('settings.json', 'r') as myfile:
  data = myfile.read()

obj = json.loads(data)

DiscordToken = str(obj['TOKEN'])
gid = str(obj['gid'])
uid = str(obj['uid'])
SpotifyToken = str(obj['SpotifyToken'])
SpotifyDeviceID = str(obj['SpotifyDeviceID'])

# spotify_client = SpotifyClient(os.getenv('SPOTIFY_TOKEN'))

# allows to run this script on windows
if not os.name == "nt":
  from pixel_ring import pixel_ring
  from gpiozero import LED

  power = LED(5)
  power.on()
  pixel_ring.set_brightness(10)

wakeword = ["raspberry ", "rsp ", "hairspray ", "harrislee ", "restaurant "]

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
      elif "danke" in Text:
        SpeechText = "Bitte"
      elif "ich bin so gut" in Text:
        SpeechText = "G U H T"
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
      elif x + "lösch mich" in Text or x + "flash mich" in Text:
        print("löschen")
        conn = http.client.HTTPSConnection("discordapp.com")
        payload = json.dumps({
          "channel_id": None
        })
        headers = {
          'Authorization': DiscordToken,
          'Content-Type': 'application/json',
        }
        conn.request("PATCH", "/api/v6/guilds/" + gid +
                     "/members/" + uid, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
      elif x + "pausiere meine musik" in Text:
        SpeechText = ("Ok")
        headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
      	  'Authorization': SpotifyToken,
        }

        params = (
          ('device_id', SpotifyDeviceID),
        )

        response = requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers, params=params)
      elif x + "setze meine musik fort" in Text:
        SpeechText = ("Ok")
        headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': SpotifyToken,
        }

        params = (
          ('device_id', SpotifyDeviceID),
        )

        data = '{"context_uri":"spotify:album:5ht7ItJgpBH7W6vJ5BqpPr","offset":{"position":5},"position_ms":0}'

        response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, params=params, data=data)
      elif x + "überspring den track" in Text or x + "überspringe den track" in Text or x + "überspringen track" in Text:
        SpeechText = ("Ok")
        headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': SpotifyToken,
        }

        params = (
          ('device_id', SpotifyDeviceID),
        )

        response = requests.post('https://api.spotify.com/v1/me/player/next', headers=headers, params=params)
      else:
        pass

  except sr.UnknownValueError:
    print("Ich konnte dich nicht verstehen!")
  except sr.RequestError:
    pass

  try:
    if SpeechText != "":
      if not os.name == "nt":
        pixel_ring.wakeup()

      speak(SpeechText)

      if not os.name == "nt":
        pixel_ring.off()
  except Exception as e:
    print("Error")

power.off()
