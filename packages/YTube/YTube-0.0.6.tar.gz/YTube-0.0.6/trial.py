from pytube import YouTube
from moviepy.editor import *

link = 'https://www.youtube.com/watch?v=JQVmkDUkZT4'
url = YouTube(str(link))
title = url.title
print(title)
video = url.streams.filter(file_extension='mp4', res= '1080p')
print(video)