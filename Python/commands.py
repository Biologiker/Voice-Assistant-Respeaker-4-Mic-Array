def was_geht():
  Text = "Ich mag dich nicht"
  print("Hey")
  return Text

def danke():
  Text = "bitte"
  return Text

def gut():
  Text = "g u h t"
  return Text

def uhrzeit(time):
  Text = "Es ist " + time.strftime('%H:%M:%S', time.localtime())
  return Text

def datum(time):
  Text = "Heute ist der " + time.strftime('%Y-%m-%d', time.localtime())
  return Text

def backflip():
  Text = "Wuuu Backflip"
  return Text
  
def spotify_pause(SpotifyToken, SpotifyDeviceID, requests):
  n = ("Ok")
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': "Bearer " + SpotifyToken,
  }

  params = (
    ('device_id', SpotifyDeviceID),
  )

  requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers, params=params)
  return n

def spotify_play(SpotifyToken, SpotifyDeviceID, requests):
  n = ("Ok")
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': "Bearer " + SpotifyToken,
  }

  params = (
    ('device_id', SpotifyDeviceID),
  )

  requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, params=params)
  return n

def spotify_skip(SpotifyToken, SpotifyDeviceID, requests):
  n = ("Ok")
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': "Bearer " + SpotifyToken,
  }

  params = (
    ('device_id', SpotifyDeviceID),
  )

  requests.post('https://api.spotify.com/v1/me/player/next', headers=headers, params=params)
  return n

def spotify_devices(DeviceList, json, TimerSpotifyDevices):
  DeviceList.pop()
  DeviceNamesEinzahl = ["Dein verfügbares Gerät ist:"]
  DeviceNames = ["Deine verfügbaren Geräte sind"]
  for x in DeviceList:
    TimerSpotifyDevices = TimerSpotifyDevices + 1
    DeviceName = x.split("name")[1].split("'")[2]
    DeviceNamesEinzahl.append(DeviceName)
    DeviceNames.append("Gerät Nummer: " + str(TimerSpotifyDevices) + ":" + DeviceName)
  
  if(TimerSpotifyDevices > 1):
    Text = DeviceNames
  else:
    Text = DeviceNamesEinzahl

  return str(Text)

def error():
  n = ("Ich habe dich nicht verstanden")
  return n