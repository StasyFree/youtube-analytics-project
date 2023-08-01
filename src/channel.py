import os
import json
from googleapiclient.discovery import build


class Channel:
    API_KEY = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.channel_descr = channel['items'][0]['snippet']['description']
        self.url = "https://www.youtube.com/" + channel['items'][0]['snippet']['customUrl']
        self.quantity_sub = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.quantity_all_vievs = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.quantity_sub) + int(other.quantity_sub)

    def print_info(self) -> None:
        """Выводит в консоль информацию python -m venv venvо канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @staticmethod
    def get_service():
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def to_json(self, filename):
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'channel_descr': self.channel_descr,
            'url': self.url,
            'quantity_sub': self.quantity_sub,
            'video_count': self.video_count,
            'quantity_all_vievs': self.quantity_all_vievs,
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)
