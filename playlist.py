
import requests
import json
import random

auth_token = 'BQAACdiqnu5IGcNz8YSIbZtjxFzvC62mesmfxEqb6qnAub7NRKsTvicF2foFu7ayWfs4P_AupjakjhBJOMzioTEfv2Ol4zak3XHuVPDkWsAQomyYtieI-X9Q8JHBy1Onf_YxF-kaMdpVjCvhcycoP-8BckLSbLUesUIp_XclkaaKO4kGPBvoIw15ZFmKlPNkd-5pLj95qscHwVhiBA'
def getTimeMS(activity, intensity, distance):
    d = float(distance)
    if activity == 'Bike':
        bikeL = 10
        bikeN = 14
        bikeH = 17

        if(intensity == 'Leisurely'):
            t = d / bikeL
        
        if(intensity == 'Normal'):
            t = d / bikeN
        
        if(intensity == 'High'):
            t = d / bikeH
        
    if activity == 'Walk':
        walkL = 2.7
        walkN = 3.0
        walkH = 3.3

        if(intensity == 'Leisurely'):
            t = d / walkL
        
        if(intensity == 'Normal'):
            t = d / walkN
        
        if(intensity == 'High'):
            t = d / walkH
        
    if activity == 'Run':
        runL = 4.5
        runN = 6
        runH = 7.5

        if(intensity == 'Leisurely'):
            t = d / runL
        
        if(intensity == 'Normal'):
            t =  d / runN
        
        if(intensity == 'High'):
            t =  d / runH
        
    return t * 60 * 60 * 1000 # convert to ms

def makeShower():
    req_url = "https://api.spotify.com/v1/playlists/0qJze4CfMAUjkzVUjOqgtX/tracks?fields=items(track(name%2C%20artists(name)%2C%20duration_ms%2C%20id))"
    js = requests.get(url=req_url, headers={
        "Authorization": "Bearer " + auth_token, "Content-Type": "application/json", "Accept": "application/json"}).json()
    song = random.choice(js['items'])
    return song
    

def makePlaylist(activity, intensity, distance, genre):

    if(genre == 'Happy'):
        playlistID = '0UdATBvU58ZxP7OC5JQW7D'
    if(genre == 'Moody'):
        playlistID = '6DceDUOjBjniEPOP4dwbQp'
    if(genre == 'Calm'):
        playlistID = '7EzTXyLxvj4A4q2ifLCZ3P'

    req_url = "https://api.spotify.com/v1/playlists/" + playlistID + "/tracks?fields=items(track(name%2C%20artists(name)%2C%20duration_ms%2C%20id))"

    js = requests.get(url=req_url, headers={
        "Authorization": "Bearer " + auth_token, "Content-Type": "application/json", "Accept": "application/json"}).json()


    # print(activity + intensity + distance + genre)
    time = getTimeMS(activity, intensity, distance)


    totalTime = 0
    songs = []
    done = False
    while(not done):
        song = random.choice(js['items'])
        if(totalTime + song['track']['duration_ms'] >= time):
            timeLeft = time - totalTime
            if(timeLeft > 60 * 1000):
                song = random.choice(js['items'])
                curTime = song['track']['duration_ms']
                songsIndexed = 0
                while(curTime > timeLeft and songsIndexed < 100):
                    song = random.choice(js['items'])
                    curTime = song['track']['duration_ms']
                    songsIndexed+=1
                songs.append(song)
            done = True
        elif(song not in songs):
            totalTime += song['track']['duration_ms']
            songs.append(song)


    print("TIME TO FILL: " + str(time))

    timePlaylist = 0
    for song in songs:
        artists = []
        for artist in song['track']['artists']:
            artists.append(artist['name'])
        
        timePlaylist += song['track']['duration_ms']

        print(song['track']['name'] + " by " + str(artists) + "(Length: " + str(song['track']['duration_ms']))

    print("TIME PLAYLIST: " + str(timePlaylist))

    

    return songs, timePlaylist, time

