import requests
from bs4 import BeautifulSoup
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SetlistScraper:
    track_text = "track:"
    artist_text = " artist:"

    def __init__(self):
        self.setlist = []

    def grab_setlist(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        for div in soup.find_all("div", attrs={"class": "songPart"}):
            song = div.text
            self.setlist.append(song.strip())
        print(self.setlist, '\n')
    
    def set_setlist(self, setlist):
        self.setlist = setlist

    def define_spotify_credentials(self, username, CLIENT_ID, CLIENT_SECRET):
        self.username = username
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.CLIENT_ID,
                client_secret=self.CLIENT_SECRET,
                redirect_uri="http://localhost:1410/",
                scope="playlist-modify-public",
            )
        )

    def create_spotify_playlist(self, playlist_name, artist):
        playlist = self.sp.user_playlist_create(self.username, playlist_name)
        playlist_id = playlist["id"]

        for song in self.setlist:
            song_text = self.track_text + song + self.artist_text + artist
            song_info = self.sp.search(q=song_text, type="track")
            if len(song_info["tracks"]["items"]) > 0:
                uri = song_info["tracks"]["items"][0]["uri"]
                self.sp.playlist_add_items(playlist_id=playlist_id, items=[uri])
                print(song + " added to playlist")
            else:
                pass
    
    def add_song_to_spotify_playlist(self, song_name, playlist_name):
        # Search for song on Spotify
        song_info = self.sp.search(q=song_name, type='track')
        if len(song_info['tracks']['items']) == 0:
            print("Failed to find ", song_name, " on Spotify.")
            return
        song_id = song_info['tracks']['items'][0]['id']
        
        # Get playlist ID
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break
        
        # Check if song is already in playlist
        playlist_tracks = self.sp.playlist_tracks(playlist_id)
        for track in playlist_tracks['items']:
            if track['track']['id'] == song_id:
                print(song_name, "already exists in playlist.")
                return
        
        # Add song to playlist
        self.sp.playlist_add_items(playlist_id, [song_id])
        print(song_name, "added to playlist!")

    def add_setlist_to_spotify_playlist(self, playlist_name):
        pass