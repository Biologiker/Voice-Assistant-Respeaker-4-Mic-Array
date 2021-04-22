def data(webbrowser, ready, requests, json):
  try:
    with open('refreshToken.json', 'r') as refreshTokenFile:
      refreshTokenData = refreshTokenFile.read()

    refreshTokenObj = json.loads(refreshTokenData)[0]

    RefreshToken = str(refreshTokenObj['refreshToken'])
  except:
    RefreshToken = ""

  if RefreshToken == "":
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
          pass  

    url = "https://accounts.spotify.com/api/token"

    payload='grant_type=authorization_code&code=' + SpotifyID + '&redirect_uri=http%3A%2F%2Fexample.com%2F'
    headers = {
      'Authorization': 'Basic Nzc2ZTZkNDEzNzM5NDRmNGEzNjViMWNmZjBjNDBiZDk6ZDY5N2Q3MjQyN2M1NGE1YmI0YjQ3MDg2MGVkZTdlNWU=',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': '__Host-device_id=AQCges5p4n0S9iC--ZQb9nb6V9mg7nm1fKKrvu1f-5_mEU2mCqZZ5e6EcQVpPgD7wlilkN_C1sJyaUolWd0oBVexlcw59-kY6bI'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    SpotifyToken = response.text.split(",")[0].split('"')[3]
    RefreshToken = response.text.split(",")[3].split('"')[3]

    #save Refresh Token to Json File
    data = {}
    data = []
    data.append({
        'refreshToken': RefreshToken,
    })

    with open('refreshToken.json', 'w') as myfile:
      json.dump(data, myfile)
  else:
    url = "https://accounts.spotify.com/api/token"

    payload='grant_type=refresh_token&refresh_token=' + RefreshToken
    headers = {
      'Authorization': 'Basic Nzc2ZTZkNDEzNzM5NDRmNGEzNjViMWNmZjBjNDBiZDk6ZDY5N2Q3MjQyN2M1NGE1YmI0YjQ3MDg2MGVkZTdlNWU=',
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responseSplit = response.text.split(",")
    SpotifyToken = responseSplit[0].split('"')[3]

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
  ready = True
  return SpotifyToken, SpotifyDeviceID, ready