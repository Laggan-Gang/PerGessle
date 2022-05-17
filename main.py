import discord
import os
import random
import filters

from dotenv import load_dotenv
from constants import KAREOKE, SONGS_METADATA_DICT



load_dotenv()


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
    songs = KAREOKE
    no_replace = False
    include_id = False

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
        msg += "PerGessle --include-id: Includes the local id to the song.\n"
        msg += "PerGessle --help: This message.\n"
        msg += "also, if you don't know, just go for pergessle good songs or pergessle popular."
        return msg
    elif input.upper().startswith("PerGessle PHIL COLLINS"):
        return "Phil Collins -- You can't hurry love, obviously."
    elif input.lower().startswith("pergessle good songs"):
        input = "pergessle --release_after 1990 --release_before 2020 --song_popularity 60 --artist_popularity 40"
        msg += f"GOOD SONGS YOU SAY? DEFAULTING TO \n > {input} \n\n"
    elif input.lower().startswith("pergessle popular"):
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


    filter_mapping = {
        "artist": filters.filter_artist,
        "song": filters.filter_song,
        "genre": filters.filter_genre,
        "artist_popularity": filters.filter_artist_popularity,
        "song_popularity": filters.filter_song_popularity,
        "release_after": filters.filter_release_after,
        "release_before": filters.filter_release_before,
    }
    arg_splits = input.split("--")

    for splits in arg_splits[1:]:
        splits = splits.strip()
        splits = splits.split(" ", 1)
        command = splits[0].lower()
        if len(splits) > 1:
            input = splits[1].lower()
            if command in filter_mapping:
                songs, msg = filter_mapping[command](songs, msg, input)
            elif command == "amount":
                amount = int(input)

        if command == "no-replace":
            no_replace = True
        elif command == "quiet":
            quiet = True
        elif command == "include-uri":
            include_uri = True
        elif command == "include-id":
            include_id = True


    msg += "\n"
    
    if quiet:
        msg = ".\n"
        
    if len(songs) == 0:
        msg += "\n*No artists/songs found, please specify a better querry.*\n"
        return msg
    
    if no_replace:
        res = random.sample(songs, k=min(amount, len(songs)))
    else:
        res = random.choices(songs, k=amount)
 

    if include_uri:
        uris = [SONGS_METADATA_DICT.get((song[1].lower(), song[2].lower()), {}).get("uri", "") for song in songs]
        msg += f"uris: {uris}\n"

    if include_id:
        res = [f"{r[1]}: {r[2]}, {r[0]}" for r in res]
    else:
        res = [f"{r[1]}: {r[2]}" for r in res]
    msg += "Songs: \n> " + "\n> ".join(res)
    print(msg)
    return msg


client.run(TOKEN)

