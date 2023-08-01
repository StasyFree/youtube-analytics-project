import os
import json
import isodate
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    API_KEY = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    like_count = 0

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.__total_duration = timedelta(0)
        playlists = self.youtube.playlists().list(part='snippet', id=self.playlist_id,
                                                  maxResults=50).execute()

        self.title = playlists['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlists['items'][0]['id']
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails', maxResults=50).execute()
        # получить все id видеороликов из плейлиста
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)) \
            .execute()
        self.best_video = ''

    @property
    def total_duration(self):

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration_video = isodate.parse_duration(iso_8601_duration)
            self.__total_duration += duration_video
        return self.__total_duration

    def show_best_video(self):

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            like_count = video['statistics']['likeCount']
            if int(like_count) > self.like_count:
                self.best_video = 'https://youtu.be/' + video['id']
        return self.best_video

