# PerGessle
Karaoke bot for discord

# Usage
Add discord-bot token to .env, under TOKEN.

> python main.py 

to run the bot.


To refetch spotify-data, set the corresponding SPOTIPY env-variables from your spotify developer app in .env.

# Commands
PerGessle: Returns 3 songs from full song list.
  --song [SEARCH_QUERY]: Returns 3 songs from songs with [SEARCH_QUERY] in them.
  --artist [SEARCH_QUERY]: Returns 3 songs from artists with [SEARCH_QUERY] in them.
  --amount [N_SONGS]: Returns [N_SONGS] songs from full song list. 
  --artist_popularity [VAL 0-100] 
  --song_popularity [VAL 0-100] 
  --release_before [YEAR] 
  --release_after [YEAR] 
  --no-replace: Sets flag to use no replacement, e.g. we can't get the same song twice.
  --quiet: Hides extra msg information except the songs.
  --include-uri: Includes a spotify uri to the song if exists.
  --include-id: Includes the local id to the song.
  --help: This message.
