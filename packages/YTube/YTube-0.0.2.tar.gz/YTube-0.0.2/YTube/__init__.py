from pytube import YouTube

def Download(link):

    url = YouTube(str(link))
    video = url.streams.first()
    video.download()
    return "Done"
