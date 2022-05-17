from constants import *
from datetime import datetime


def filter_artist(songs, msg, input):
    artists = [ak for ak in ARTISTS_KARAOKE.keys() if input in ak.lower()]
    songs = [song for song in songs if input in song[1].lower()]

    if len(artists) and len(artists) < 5:
        msg += f"Found artists, {len(artists)}: " + ", ".join(artists) + f" with {len(songs)} songs.\n"
    elif artists:
        msg += f"Found artists, {len(artists)} with {len(songs)} songs, too many to write.\n"

    return songs, msg

def filter_song(songs, msg, input):
    songs = [song for song in songs if input in song[2].lower()]
    if len(songs) and len(songs) < 5:
        songs_to_write = [f"{song[1]}: {song[2]}" for song in songs]
        msg += f"Found songs, {len(songs)}: " + ", ".join(songs_to_write) + ".\n"
    elif songs:
        msg += f"Found songs, {len(songs)}, too many to write.\n"
    
    return songs, msg

def filter_genre(songs, msg, input):
    genre = input
    new_songs = []
    genres = set()
    artists = set()
    for song in songs:
        artist = song[1]
        metadata = ARTISTS_METADATA_DICT.get(artist.lower(), {})
        artist_genres = metadata.get("genres", [])
        if any([genre in artist_genre for artist_genre in artist_genres]):
            genres.update([artist_genre for artist_genre in artist_genres if genre in artist_genre])
            new_songs.append(song)
            artists.add(artist)
    
    songs = new_songs
    
    if songs and len(genres) <= 10:
        msg += f"Found songs with artist under genre {genre}, found in {genres}!! {len(songs)} songs from {len(artists)} artists.\n"
    elif songs and len(genres) > 10:
        msg += f"Found songs with artist under genre {genre}, found in more than {list(genres)[:10]}!! Exact amount of genres = {len(genres)}. {len(songs)} songs from {len(artists)} artists.\n"
    else:
        msg += f"Found no songs with genre {genre}!!\n"
    
    return song, msg

def filter_artist_popularity(songs, msg, input):
    threshold = int(input)
    new_songs = []
    artists = set()
    for song in songs:
        artist = song[1]
        metadata = ARTISTS_METADATA_DICT.get(artist.lower(), {})
        populartiy = metadata.get("popularity", 0)
        if populartiy >= threshold:
            new_songs.append(song)
            artists.add(artist)
    
    songs = new_songs
    if songs:
        msg += f"Found popular artists over {threshold}!! {len(songs)} songs from {len(artists)} artists.\n"
    else:
        msg += f"Found no popular artists over {threshold}!!\n"
    
    return songs, msg


def filter_song_popularity(songs, msg, input):
    threshold = int(input)
    new_songs = []
    artists = set()
    for song_tuple in songs:
        artist = song_tuple[1]
        song = song_tuple[2]
        metadata = SONGS_METADATA_DICT.get((artist.lower(), song.lower()), {})
        populartiy = metadata.get("popularity", 0)
        if populartiy >= threshold:
            new_songs.append(song_tuple)
            artists.add(artist)
    
    songs = new_songs
    if songs:
        msg += f"Found popular songs over {threshold}!! {len(songs)} songs from {len(artists)} artists.\n"
    else:
        msg += f"Found no popular songs over {threshold}!!\n"
    
    return songs, msg


def filter_release_after(songs, msg, input):
    parse_res = parser.parse(input, fuzzy=True)
    if not parse_res:
        msg += f"Could not parse {input} for a year, ignoring release after.\n"
        return songs, msg

    date = datetime(parse_res.year, 1, 1)
    songs = [song for song in songs if SONGS_DATETIME.get((song[1].lower(), song[2].lower()), datetime(1970, 1, 1)) >= date]
    if songs:
        msg += f"Found {len(songs)} songs released after {date.year}.\n"

    return songs, msg

def filter_release_before(songs, msg, input):
    parse_res = parser.parse(input, fuzzy=True)
    if not parse_res:
        msg += f"Could not parse {input} for a year, ignoring release before.\n"
        return songs, msg 

    date = datetime(parse_res.year, 1, 1)
    songs = [song for song in songs if SONGS_DATETIME.get((song[1].lower(), song[2].lower()), datetime(2125, 1, 1)) <= date]

    if songs:
        msg += f"Found {len(songs)} songs released before {date.year}.\n"
    
    return songs, msg

