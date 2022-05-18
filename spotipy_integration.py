import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# DATA_FOLDER = os.path.join(os.path.realpath('.'), "data/")
DATA_FOLDER = "./"
KAREOKE = json.load(open(DATA_FOLDER + "kkareoke_songs.json", "r"))
artists = list(set([song[1] for song in KAREOKE]))
songs = list([(song[1], song[2]) for song in KAREOKE])


def fetch_songs():
    items_not_found = []
    song_metadata = []
    for artist, song in songs:
        query = song + ' artist:' + artist
        print(query)
        results = spotify.search(q=query, type='track')

        items = results['tracks']['items']
        if not items:
            query = song
            print(query)
            results = spotify.search(q=query, type='track')
            items = results['tracks']['items']

        if not items:
            items_not_found.append((artist, song))
            continue

        item = items[0]

        release_date = item["album"]["release_date"]
        name = item["name"]
        popularity = item["popularity"]
        uri = item["uri"]
        song_metadata.append(
            { 
                "song": (artist, song),
                "name": name, 
                "release": release_date,
                "popularity": popularity,
                "uri": uri,
            })

    json.dump(song_metadata, open(DATA_FOLDER + "songs_metadata.json", "w"))
    json.dump(items_not_found, open(DATA_FOLDER + "missed_songs.json", "w"))

def fetch_artists():
    out = []
    missed_entries = []
    for name in artists:
        results = spotify.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            print(artist)
            uri = artist["uri"]
            genres = artist["genres"]
            popularity = artist["popularity"]
            followers = artist["followers"]["total"]
            url = artist["external_urls"]["spotify"]
            out.append(
                {
                    "name": name, 
                    "uri": uri, 
                    "genres": genres, 
                    "popularity": popularity,
                    "followers": followers,
                    "url": url
                })
        else:
            missed_entries.append(name)

    json.dump(out, open(DATA_FOLDER + "artists_metadata.json", "w"))
    json.dump(missed_entries, open(DATA_FOLDER + "missed_artists.json", "w"))

if __name__ == "__main__":
    fetch_artists()
    fetch_songs()