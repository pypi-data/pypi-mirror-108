from pytube import YouTube
from moviepy.editor import *
import os


#Download the default video resolution
#-------------------------------------
def download(link):

    url = YouTube(str(link))
    video = url.streams.first()
    video.download()
    return "Done"


#Download quickest high quality version
#--------------------------------------
def fastDownload(link):

    url = YouTube(str(link))
    video = url.streams.get_highest_resolution()
    video.download()
    return "Done"


#Download 144p quality
#---------------------
def download_144(link):

    try:
        url = YouTube(str(link))
        title = url.title
        video = url.streams.filter(file_extension='mp4', res= '144p').first()
        finalOutput(video, title, link)

    
    except Exception:
        print("Resolution not available")
    return "Done"


#Download 360p quality
#----------------------
def download_360(link):

    try:
        url = YouTube(str(link))
        title = url.title
        video = url.streams.filter(file_extension='mp4', res= '360p').first()
        finalOutput(video, title, link)
    

    except Exception:
        download_144(link)
    return "Done"


#Download 480p quality
#----------------------
def download_480(link):

    try:
        url = YouTube(str(link))
        title = url.title
        video = url.streams.filter(file_extension='mp4', res= '480p').first()
        finalOutput(video, title, link)

    
    except Exception:
        download_360(link)
    return "Done"


#Download 720p quality
#----------------------
def download_720(link):

    try:
        url = YouTube(str(link))
        title = url.title
        video = url.streams.filter(file_extension='mp4', res= '720p').first()
        finalOutput(video, title, link)

    
    except Exception:
        download_480(link)
    return "Done"


#Download 1080p quality
#----------------------
def download_1080(link):
    try:
        url = YouTube(str(link))
        title = url.title
        video = url.streams.filter(file_extension='mp4', res= '1080p').first()
        finalOutput(video, title, link)

    
    except Exception:
        download_720(link)
    return "Done"


#Merge audio and video. Save final video
#---------------------------------------
def finalOutput(video, title, link):

    url = YouTube(str(link))

    out_file = video.download(output_path = '.')
    base, ext = os.path.splitext(out_file)
    new_file = "video" + ".mp4"
    os.rename(out_file, new_file)


    audio = url.streams.get_audio_only()

    out_file = audio.download(output_path = '.')
    base, ext = os.path.splitext(out_file)
    new_file = "audio" + ".mp3"
    os.rename(out_file, new_file)



    clip = VideoFileClip("video.mp4")
    audioclip = AudioFileClip("audio.mp3")

    videoclip = clip.set_audio(audioclip)
    videoclip.write_videofile(title + ".mp4", codec='mpeg4', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

    os.remove("video.mp4")
    os.remove("audio.mp3")
