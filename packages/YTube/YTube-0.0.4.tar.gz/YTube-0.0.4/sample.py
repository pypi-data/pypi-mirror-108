import pytube

url = 'https://www.youtube.com/watch?v=4SFhwxzfXNc'

youtube = pytube.YouTube(url)
video = youtube.streams.first()
#stream = youtube.streams.all()
yt = youtube.streams.filter(file_extension='mp4', res= '1080p')
print(yt)
#for i in stream:
 #print(i)