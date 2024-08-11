import asyncio
import os
import re
from typing import Union

from pytube import YouTube
import aiohttp

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1):
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str):
        yt = YouTube(link)
        title = yt.title
        duration_min = yt.length // 60
        duration_sec = yt.length
        thumbnail = yt.thumbnail_url
        vidid = yt.video_id
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str):
        yt = YouTube(link)
        return yt.title

    async def duration(self, link: str):
        yt = YouTube(link)
        return yt.length // 60

    async def thumbnail(self, link: str):
        yt = YouTube(link)
        return yt.thumbnail_url

    async def video(self, link: str):
        yt = YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        return 1, stream.url

    async def download(self, link: str, video: Union[bool, str] = None, songaudio: Union[bool, str] = None, songvideo: Union[bool, str] = None, title: Union[bool, str] = None) -> str:
        yt = YouTube(link)
        if songvideo:
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            fpath = f"downloads/{title}.mp4"
            stream.download(output_path="downloads", filename=f"{title}.mp4")
            return fpath
        elif songaudio:
            stream = yt.streams.filter(only_audio=True).first()
            fpath = f"downloads/{title}.mp3"
            stream.download(output_path="downloads", filename=f"{title}.mp3")
            return fpath
        elif video:
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            fpath = f"downloads/{title}.mp4"
            stream.download(output_path="downloads", filename=f"{title}.mp4")
            return fpath
        else:
            stream = yt.streams.filter(only_audio=True).first()
            fpath = f"downloads/{title}.mp3"
            stream.download(output_path="downloads", filename=f"{title}.mp3")
            return fpath
