import json
from dateutil import parser
KAREOKE = json.load(open("kkareoke_songs.json", "r"))
ARTISTS_METADATA = json.load(open("artist_metadata.json", "r"))
SONGS_METADATA = json.load(open("songs_metadata.json", "r"))

ARTISTS_METADATA_DICT = {md["name"].lower(): md for md in ARTISTS_METADATA}
SONGS_METADATA_DICT = {(md["song"][0].lower(), md["song"][1].lower()): md for md in SONGS_METADATA}

ARTISTS_KARAOKE = {}
ARTISTS = list(set([song[1] for song in KAREOKE]))
SONGS_DATETIME = {(entry["song"][0].lower(), entry["song"][1].lower()): parser.parse(entry["release"], fuzzy=True) for entry in SONGS_METADATA}

for id, artist, song in KAREOKE:
    if artist not in ARTISTS_KARAOKE:
        ARTISTS_KARAOKE[artist.lower()] = []

    ARTISTS_KARAOKE[artist.lower()].append((id, artist, song))

