from pytube import YouTube
import ffmpeg
from sys import argv
from pathlib import Path


def clean_filename(name):
    forbidden_chars = '"*\\/\'.|?:<>'
    filename = (''.join([x if x not in forbidden_chars else '#' for x in name])).replace('  ', ' ').strip()
    if len(filename) >= 176:
        filename = filename[:170] + '...'
    return filename

dest_path = argv[1]
print(dest_path)
link = argv[2]
print(link)
if len(argv) > 3:
    res = argv[3]

yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
print('Title: ' + yt.title)

print('Downloading...')

vid_path = Path(__file__).parent / './video.mp4'
aud_path = Path(__file__).parent / './audio.mp3'

dynamic_streams = ['2160p|160kbps', '1440p|160kbps', '1080p|160kbps', '720p|160kbps', '720p|128kbps', '480p|160kbps', '480p|128kbps']

for ds in dynamic_streams:
    try:
        if len(argv) > 3:
            if ds.split('|')[0] != res:
                continue
        yt.streams.filter(res=ds.split('|')[0], progressive=False).first().download(filename=vid_path)
        yt.streams.filter(abr=ds.split('|')[1], progressive=False).first().download(filename=aud_path)
        break
    except (Exception):
        continue

video = ffmpeg.input(vid_path)
audio = ffmpeg.input(aud_path)

filename = dest_path + './' + clean_filename(yt.title) + '.mp4'
ffmpeg.output(audio, video, filename).run()

print('Done')