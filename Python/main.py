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
import webbrowser

#Spotify activation
ready = False

webbrowser.open('https://accounts.spotify.com/authorize?client_id=776e6d41373944f4a365b1cff0c40bd9&redirect_uri=http://example.com/&response_type=code&scope=user-read-private%20user-read-email%20ugc-image-upload%20user-read-recently-played%20user-top-read%20user-read-playback-position%20user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing%20app-remote-control%20streaming%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20playlist-read-collaborative%20user-follow-modify%20user-follow-read%20user-library-modify%20user-library-read')
#show_dialog=true&

while(ready == False):
  print("Your Redirected Website")
  InputText = input()
  if("example.com" in InputText):
    SpotifyID = InputText.split("=")[1]
    if(SpotifyID == "access_denied"):
      print("You must accept!")
      webbrowser.open('https://accounts.spotify.com/authorize?client_id=776e6d41373944f4a365b1cff0c40bd9&redirect_uri=http://example.com/&response_type=code&scope=user-read-private%20user-read-email%20ugc-image-upload%20user-read-recently-played%20user-top-read%20user-read-playback-position%20user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing%20app-remote-control%20streaming%20playlist-modify-public%20playlist-modify-private%20playlist-read-private%20playlist-read-collaborative%20user-follow-modify%20user-follow-read%20user-library-modify%20user-library-read')
    else:
      ready = True   

url = "https://accounts.spotify.com/api/token"

payload='grant_type=authorization_code&code=' + SpotifyID + '&redirect_uri=http%3A%2F%2Fexample.com%2F'
headers = {
  'Authorization': 'Basic Nzc2ZTZkNDEzNzM5NDRmNGEzNjViMWNmZjBjNDBiZDk6ZDY5N2Q3MjQyN2M1NGE1YmI0YjQ3MDg2MGVkZTdlNWU=',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': '__Host-device_id=AQCges5p4n0S9iC--ZQb9nb6V9mg7nm1fKKrvu1f-5_mEU2mCqZZ5e6EcQVpPgD7wlilkN_C1sJyaUolWd0oBVexlcw59-kY6bI'
}

response = requests.request("POST", url, headers=headers, data=payload)
SpotifyToken = response.text.split(",")[0].split('"')[3]

#get Active Device ID
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + SpotifyToken,
}

response = requests.get('https://api.spotify.com/v1/me/player/devices', headers=headers)
responseJson = response.json()
responseSplit = str(responseJson['devices']).split("[")[1].split("]")[0].split("}")

for x in responseSplit:
  if len(x) > 10:
    x = x.split("{")[1] 
    if "'is_active': True" in x:
      ActiveDevice = x

SpotifyDeviceID = ActiveDevice.split(",")[0].split(":")[1].split("'")[1]

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
        SpeechText = commands.spotify_pause(SpotifyToken, SpotifyDeviceID, requests)
      elif x + "setze meine musik fort" in Text or x + "setze musik fort" in Text or x + "setze meine musik vor" in Text or x + "meine musik fort" in Text:
        SpeechText = commands.spotify_play(SpotifyToken, SpotifyDeviceID, requests)
      elif x + "überspringe diesen song" in Text or x + "überspringe den track" in Text or x + "überspringen track" in Text or x + "überspring den dreck" in Text or x + "überspringe den dreck" in Text or x + "überspringen dreck" in Text:
        SpeechText = commands.spotify_skip(SpotifyToken, SpotifyDeviceID, requests)
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