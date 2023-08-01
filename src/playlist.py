import os
import json
from googleapiclient.discovery import build


class PlayList:
    API_KEY = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlists = self.youtube.playlists().list(part='contentDetails, snippet', id=self.playlist_id,
                                                  maxResults=50).execute()
        print(json.dumps(playlists, indent=2, ensure_ascii=False))

        self.title = playlists['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlists['items'][0]['id']
