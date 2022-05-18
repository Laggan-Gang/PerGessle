import json
import os
from dateutil import parser

#_DATA_FOLDER = os.path.join(os.path.realpath('.'), "data")
_DATA_FOLDER = "."
_SONG_LIST_PATH = os.path.join(_DATA_FOLDER, "kkareoke_songs.json")
_ARTISTS_METADATA_PATH = os.path.join(_DATA_FOLDER, "artists_metadata.json")
_SONGS_METADATA_PATH = os.path.join(_DATA_FOLDER, "songs_metadata.json")

KAREOKE = json.load(open(_SONG_LIST_PATH, "r"))
ARTISTS_METADATA = json.load(open(_ARTISTS_METADATA_PATH, "r"))
SONGS_METADATA = json.load(open(_SONGS_METADATA_PATH, "r"))

ARTISTS_METADATA_DICT = {md["name"].lower(): md for md in ARTISTS_METADATA}
SONGS_METADATA_DICT = {(md["song"][0].lower(), md["song"][1].lower()): md for md in SONGS_METADATA}

ARTISTS_KARAOKE = {}
ARTISTS = list(set([song[1] for song in KAREOKE]))
SONGS_DATETIME = {(entry["song"][0].lower(), entry["song"][1].lower()): parser.parse(entry["release"], fuzzy=True) for entry in SONGS_METADATA}

for id, artist, song in KAREOKE:
    if artist not in ARTISTS_KARAOKE:
        ARTISTS_KARAOKE[artist.lower()] = []

    ARTISTS_KARAOKE[artist.lower()].append((id, artist, song))

