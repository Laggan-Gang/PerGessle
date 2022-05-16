import discord
import os
import json
import random

from datetime import datetime
from dotenv import load_dotenv
from dateutil import parser

load_dotenv()

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


TOKEN = os.getenv("TOKEN")
client = discord.Client()

@client.event
async def on_ready():
    print(f"User: {client.user} DET VERKAR SÅ LÄTT ATT BARA STÖTA PÅ, DET ÄR ALLA MÄNISKORS RÄTT, ATT BARA GÖR SÅ!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(client.user, message.author)
    msg = message.content
    
    if msg.lower().startswith("pergessle"):
        to_send = pergessle(msg)
        await message.channel.send(to_send)
        return

def pergessle(input):
    amount = 3
    songs = []
    quiet = False
    include_uri = False

    msg = ".\n"
    if input.lower().startswith("pergessle --help")  or input.lower().startswith("pergessle help"):
        msg += "Commands available:\n"
        msg += "PerGessle: Returns 3 songs from full song list.\n"
        msg += "PerGessle --song [SEARCH_QUERY]: Returns 3 songs from songs with [SEARCH_QUERY] in them.\n"
        msg += "PerGessle --artist [SEARCH_QUERY]: Returns 3 songs from artists with [SEARCH_QUERY] in them.\n"
        msg += "PerGessle --amount [N_SONGS]: Returns [N_SONGS] songs from full song list. \n"
        msg += "PerGessle --artist_popularity [VAL 0-100] \n"
        msg += "PerGessle --song_popularity [VAL 0-100] \n"
        msg += "PerGessle --release_before [YEAR] \n"
        msg += "PerGessle --release_after [YEAR] \n"
        msg += "PerGessle --no-replace: Sets flag to use no replacement, e.g. we can't get the same song twice.\n"
        msg += "PerGessle --quiet: Hides extra msg information except the songs.\n"
        msg += "PerGessle --include-uri: Includes a spotify uri to the song if exists.\n"
        msg += "PerGessle --help: This message.\n"
        msg += "also, if you don't know, just go for pergessle good songs or pergessle popular."
        return msg

    songs = KAREOKE
    no_replace = False
    if input.upper().startswith("PerGessle PHIL COLLINS"):
        return "Phil Collins -- You can't hurry love, obviously."

    if input.lower().startswith("pergessle good songs"):
        input = "pergessle --release_after 1990 --release_before 2020 --song_popularity 60 --artist_popularity 40"
        msg += f"GOOD SONGS YOU SAY? DEFAULTING TO \n > {input} \n\n"
    
    if input.lower().startswith("pergessle popular"):
        input = "pergessle --release_after 1980 --song_popularity 70 --genre pop"
        msg += f"POPULAR SONGS YOU SAY? DEFAULTING TO \n > {input} \n\n"

    
    dennis_list = [
        "Arja Saijonmaa - Högt över havet - 990",
        "Björn Skifs - Michelangelo - 1073",
        "Bonnie Tyler - Holding out for a hero - 1387",
        "Disturbed - Down with the sickness - 5582",
        "Erasure - Stop - 4252",
        "Human League - Don't you want me - 1608",
        "Linkin Park - In the end - 839",
        "Olsen Brothers - Fly on the wings of love - 1001",
        "Pitbull Feat. Ke$ha - Timber - 5251",
        "Rasmus - In the shadows - 655",
        "Roger Pontare - Vindarna viskar mitt namn - 1009",
        "Sandi Thom - I wish I was a punkrocker - 736",
        "Sarek - Genom eld och vatten - 808",
        "Vanessa Carlton - A thousand miles - 147",
    ]

    if input.lower().startswith("pergessle dennis"):
        msg += "Your GRANTED song from 'The List of Dennis':\n"
        return msg + random.choice(dennis_list)



    arg_splits = input.split("--")

    for splits in arg_splits[1:]:
        splits = splits.strip()
        splits = splits.split(" ", 1)
        print(splits)
        if len(splits) > 1:
            if splits[0].lower() == "artist":
                
                artists = [ak for ak in ARTISTS_KARAOKE.keys() if splits[1].lower() in ak.lower()]
                songs = [song for song in songs if splits[1].lower() in song[1].lower()]

                if len(artists) and len(artists) < 5:
                    msg += f"Found artists, {len(artists)}: " + ", ".join(artists) + f" with {len(songs)} songs.\n"
                elif artists:
                    msg += f"Found artists, {len(artists)} with {len(songs)} songs, too many to write.\n"
            
            if splits[0].lower() == "song":
                songs = [song for song in songs if splits[1].lower() in song[2].lower()]
                if len(songs) and len(songs) < 5:
                    songs_to_write = [f"{song[1]}: {song[2]}" for song in songs]
                    msg += f"Found songs, {len(songs)}: " + ", ".join(songs_to_write) + ".\n"
                elif songs:
                    msg += f"Found songs, {len(songs)}, too many to write.\n"

           
            if splits[0].lower() == "genre":
                genre = splits[1]
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

            if splits[0].lower() == "artist_popularity":
                threshold = int(splits[1])
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

            if splits[0].lower() == "song_popularity":
                threshold = int(splits[1])
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
            
            if splits[0].lower() == "release_after":
                parse_res = parser.parse(splits[1], fuzzy=True)
                if not parse_res:
                    msg += f"Could not parse {splits[1]} for a year, ignoring release after.\n"
                    continue 

                date = datetime(parse_res.year, 1, 1)
                songs = [song for song in songs if SONGS_DATETIME.get((song[1].lower(), song[2].lower()), datetime(1970, 1, 1)) >= date]
                if songs:
                    msg += f"Found {len(songs)} songs released after {date.year}.\n"
            if splits[0].lower() == "release_before":
                parse_res = parser.parse(splits[1], fuzzy=True)
                if not parse_res:
                    msg += f"Could not parse {splits[1]} for a year, ignoring release before.\n"
                    continue 

                date = datetime(parse_res.year, 1, 1)
                songs = [song for song in songs if SONGS_DATETIME.get((song[1].lower(), song[2].lower()), datetime(2125, 1, 1)) <= date]

                if songs:
                    msg += f"Found {len(songs)} songs released before {date.year}.\n"

            if splits[0].lower() == "amount":
                amount = int(splits[1])

        if splits[0].lower() == "no-replace":
            no_replace = True

        if splits[0].lower() == "quiet":
            quiet = True

        if splits[0].lower() == "include-uri":
            include_uri = True


    msg += "\n"
    if len(songs) == 0:
        msg += "*No artists/songs found, defaulting to all songs.*\n\n"
        songs = KAREOKE
    
    if no_replace:
        res = random.sample(songs, k=min(amount, len(songs)))
    else:
        res = random.choices(songs, k=amount)
 
    if quiet:
        msg = ".\n\n"

    if include_uri:
        uris = [SONGS_METADATA_DICT.get((song[1], song[2]), {}).get("uri", "") for song in songs]
        msg += f"uris: {uris}\n"

    
    res = [f"{r[1]}: {r[2]}" for r in res]
    msg += "You can choose either: \n" + "\n or \n".join(res) + "."
    print(msg)
    return msg


client.run(TOKEN)

