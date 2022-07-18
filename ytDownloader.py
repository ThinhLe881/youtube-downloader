from pytube import YouTube
import ffmpeg
from sys import argv

def clean_filename(name):
    forbidden_chars = '"*\\/\'.|?:<>'
    filename = (''.join([x if x not in forbidden_chars else '#' for x in name])).replace('  ', ' ').strip()
    if len(filename) >= 176:
        filename = filename[:170] + '...'
    return filename

link = argv[1]
if len(argv) > 2:
    res = argv[2]

yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
print('Title: ' + yt.title)
print('Downloading...')

dynamic_streams = ['2160p|160kbps', '1440p|160kbps', '1080p|160kbps', '720p|160kbps', '720p|128kbps', '480p|160kbps', '480p|128kbps']
for ds in dynamic_streams:
    try:
        if len(argv) > 2:
            if ds.split('|')[0] != res:
                continue
        yt.streams.filter(res=ds.split('|')[0], progressive=False).first().download(filename='video.mp4')
        yt.streams.filter(abr=ds.split('|')[1], progressive=False).first().download(filename='audio.mp3')
        break;
    except (Exception):
        continue

audio = ffmpeg.input('audio.mp3')
video = ffmpeg.input('video.mp4')

filename = 'C:\\Users\\Thinh Le\\Downloads\\Video\\' + clean_filename(yt.title) + '.mp4'
ffmpeg.output(audio, video, filename).run()

print('Done')