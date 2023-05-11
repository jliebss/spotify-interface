# import requests
# from bs4 import BeautifulSoup
# import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyInterface:
    def __init__(self, username, CLIENT_ID, CLIENT_SECRET):
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

    def get_song_id(self, song_name, artist_name=' '):
        song_search_text = song_name + ' ' + artist_name
        song_info = self.sp.search(q=song_search_text, type="track")
        if len(song_info["tracks"]["items"]) == 0:
            print("Failed to find", song_name, "on Spotify")
            return
        song_id = song_info["tracks"]["items"][0]["id"]
        return song_id

    def get_playlist_id(self, playlist_name):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists["items"]:
            if playlist["name"] == playlist_name:
                playlist_id = playlist["id"]
                return playlist_id
        print("Failed to find", playlist_name, "on Spotify")

    def check_if_song_in_playlist(self, song_name, playlist_name):
        # song_id = self.get_song_id(song_name=song_name)
        playlist_id = self.get_playlist_id(playlist_name=playlist_name)
        playlist_tracks = self.sp.playlist_tracks(playlist_id)
        # Do I want to add text capabilities? i.e., "Song not in playlist"
        for track in playlist_tracks["items"]:
            if track["track"]["name"] == song_name:
                return True
        return False

    def add_song_to_playlist(self, song_name, playlist_name, artist_name=' ', avoid_duplicates=True):
        # Check if song is already in playlist
        if avoid_duplicates:
            if self.check_if_song_in_playlist(
                song_name=song_name, playlist_name=playlist_name
            ):
                print(song_name, "is already in the", playlist_name, "playlist")
                return
        # Grab song from Spotify
        song_id = self.get_song_id(song_name=song_name, artist_name=artist_name)
        # Get playlist ID
        playlist_id = self.get_playlist_id(playlist_name=playlist_name)
        # Add song to playlist
        self.sp.playlist_add_items(playlist_id, [song_id])
        print(song_name, "added to the", playlist_name, "playlist")

    def remove_song_from_playlist(self, song_name, playlist_name, artist_name=' '):
        pass