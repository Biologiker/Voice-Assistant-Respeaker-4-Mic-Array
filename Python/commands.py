def was_geht():
  Text = "Ich mag dich nicht"
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
  
def disconnect_discord(http, json, DiscordToken, gid, uid):
  conn = http.client.HTTPSConnection("discordapp.com")
  payload = json.dumps({
    "channel_id": None
  })
  headers = {
    'Authorization': DiscordToken,
    'Content-Type': 'application/json',
  }
  conn.request("PATCH", "/api/v6/guilds/" + gid + "/members/" + uid, payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))
  n = "Weg mit dir du Wixxa"
  return n

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

  data = '{"context_uri":"spotify:album:5ht7ItJgpBH7W6vJ5BqpPr","offset":{"position":5},"position_ms":0}'
  requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, params=params, data=data)
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

def error():
  n = ("Ich habe dich nicht verstanden")
  return n