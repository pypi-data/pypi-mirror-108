from pytube import YouTube

def download(link):

    url = YouTube(str(link))
    video = url.streams.first()
    video.download()
    return "Done"

def download_Highest(link):

    url = YouTube(str(link))
    video = url.streams.get_highest_resolution()
    video.download()
    return "Done"

def download_144(link):

    url = YouTube(str(link))
    video = url.streams.filter(file_extension='mp4', res= '144p')
    video.download()
    return "Done"

def download_360(link):

    url = YouTube(str(link))
    video = url.streams.filter(file_extension='mp4', res= '360p')
    video.download()
    return "Done"

def download_480(link):

    url = YouTube(str(link))
    video = url.streams.filter(file_extension='mp4', res= '480p')
    video.download()
    return "Done"

def download_720(link):

    url = YouTube(str(link))
    video = url.streams.filter(file_extension='mp4', res= '720p')
    video.download()
    return "Done"

def download_1080(link):

    url = YouTube(str(link))
    video = url.streams.filter(file_extension='mp4', res= '1080p')
    video.download()
    return "Done"