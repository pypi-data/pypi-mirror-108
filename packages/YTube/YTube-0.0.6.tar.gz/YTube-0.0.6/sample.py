from pytube import YouTube
from moviepy.editor import *
import os

link = 'https://www.youtube.com/watch?v=JQVmkDUkZT4'

#youtube = YouTube(url)
#video = youtube.streams.first()


url = YouTube(str(link))
title = url.title
print(title)
video = url.streams.filter(file_extension='mp4', res= '1080p').first()
print(video)
video.download()

out_file = video.download(output_path = '.')
base, ext = os.path.splitext(out_file)
new_file = "video" + ".mp4"
os.rename(out_file, new_file)


audio = url.streams.get_audio_only()
print(audio)
print("hey")

out_file = audio.download(output_path = '.')
base, ext = os.path.splitext(out_file)
new_file = "audio" + ".mp3"
os.rename(out_file, new_file)


#input_video = ffmpeg.input('./video.mp4')
#input_audio = ffmpeg.input('./audio.mp3')

print("hey")

#ffmpeg.concat(input_video, input_audio, v=1, a=1).output('download.mp4').run(overwrite = "True")

clip = VideoFileClip("video.mp4")
audioclip = AudioFileClip("audio.mp3")

videoclip = clip.set_audio(audioclip)
videoclip.write_videofile(title + ".mp4", codec='mpeg4', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

os.remove("video.mp4")
os.remove("audio.mp3")
    



#for i in yt:
 #print(i)