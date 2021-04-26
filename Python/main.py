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
import struct
import pyaudio
import pvporcupine

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

wakeword = ["raspberry ", "rsp ", "hairspray ", "harrislee ", "restaurant ", "raspberry pi "]


#Hotword Detextion (recognize Jarvis, Alexa, Hey google)
porcupine = None
pa = None
audio_stream = None#

def speak(text):
    tts = gTTS(text=text, lang="de")
    filename = "voice.mp3"
    tts.save(filename)

    song = AudioSegment.from_mp3(filename)
    play(song)

try:
  porcupine = pvporcupine.create(keywords=["jarvis"])
  pa = pyaudio.PyAudio()
  audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
  while ready == True:
    Text = ""
    SpeechText = ""
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    keyword_index = porcupine.process(pcm)
    
    
    
    if keyword_index >= 0:
      if not os.name == "nt":
        pixel_ring.wakeup()

      r = sr.Recognizer()
      with sr.Microphone() as source:
        print("Say something!")
        print()
        audio = r.listen(source)
      
      try:
        Text = r.recognize_google(audio, language='de-DE')
        Text = Text.lower()
        print(Text)

        if "was geht" in Text:
          SpeechText = commands.was_geht()
        elif "danke" in Text:
          SpeechText = commands.danke()
        elif "ich bin so gut" in Text:
          SpeechText = commands.gut()
        elif "sag meinem lehrer mal wie viel uhr es ist" in Text or "wie viel uhr ist es" in Text or "uhrzeit" in Text or "wie viel uhr ist es gerade" in Text or "wie spät ist es" in Text:
          SpeechText = commands.uhrzeit(time)
        elif "datum" in Text:
          SpeechText = commands.datum(time)
        elif "mach einen backflip" in Text:
          SpeechText = commands.backflip()
        elif "lösch mich" in Text or "flash mich" in Text or "fick mich" in Text or "rette mich" in Text:
          SpeechText = commands.disconnect_discord(http, json, DiscordToken, gid, uid)
        elif "pausiere meine musik" in Text or  "spotify pause" in Text:
          try:
            SpeechText = commands.spotify_pause(SpotifyToken, SpotifyDeviceID, requests)
          except:
            print("Spotify Error")
            spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
            SpotifyToken = spotifyResult[0]
            SpotifyDeviceID = spotifyResult[1]
            ready = spotifyResult[2]
        elif  "setze meine musik fort" in Text or  "setze musik fort" in Text or  "setze meine musik vor" in Text or  "meine musik fort" in Text or "spotify play" in Text:
          try:
            SpeechText = commands.spotify_play(SpotifyToken, SpotifyDeviceID, requests)
          except:
            print("Spotify Error")
            spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
            SpotifyToken = spotifyResult[0]
            SpotifyDeviceID = spotifyResult[1]
            ready = spotifyResult[2]
        elif "spotify skip" in Text or "überspringe diesen song" in Text or "überspringe den track" in Text or "überspringen track" in Text or "überspring den dreck" in Text or "überspringe den dreck" in Text or "überspringen dreck" in Text:
          try:
            SpeechText = commands.spotify_skip(SpotifyToken, SpotifyDeviceID, requests)
          except:
            print("Spotify Error")
            spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
            SpotifyToken = spotifyResult[0]
            SpotifyDeviceID = spotifyResult[1]
            ready = spotifyResult[2]
        elif "fick dich" in Text:
          SpeechText = "Ha hahaha aha ha"
        elif "verpissdich" in Text:
          speak("O O O O O O O O O")
          exit()
        elif "discord ton aus" in Text:
          SpeechText = commands.stumm_discord(http, json, DiscordToken, gid, uid)
        elif "discord ton an" in Text:
          SpeechText = commands.unstumm_discord(http, json, DiscordToken, gid, uid)
        elif "discord mikro aus" in Text:
          SpeechText = commands.mute_discord(http, json, DiscordToken, gid, uid)
        elif "discord mikro an" in Text:
          SpeechText = commands.unmute_discord(http, json, DiscordToken, gid, uid)
        else:
          SpeechText = commands.error()

      except sr.UnknownValueError:
        print("Ich konnte dich nicht verstehen!")
      except sr.RequestError:
        pass

      try:
        if not os.name == "nt":
          pixel_ring.think()
        if SpeechText != "":
          speak(SpeechText)
          

        if not os.name == "nt":
          pixel_ring.off()
      except Exception as e:
        print("Error")
    else:
      if not os.name == "nt":
        pixel_ring.off()
      
finally:
  if porcupine is not None:
    porcupine.delete()
  if audio_stream is not None:
    audio_stream.close()
  if pa is not None:
    pa.terminate()

power.off()