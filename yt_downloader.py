import argparse
from pytube import YouTube
import ffmpeg
import os

def clean_filename(name):
    forbidden_chars = '"*\\/\'.|?:<>'
    filename = (''.join([x if x not in forbidden_chars else '#' for x in name])).replace('  ', ' ').strip()
    if len(filename) >= 176:
        filename = filename[:170] + '...'
    return filename

def download_video(yt, res):
    print('Title: ' + yt.title)
    print('Downloading...')

    current_path = os.getcwd()
    vid_path = rf'{current_path}\video.mp4'
    aud_path = rf'{current_path}\audio.mp3'
    vid_res = ['2160p', '1440p', '1080p', '720p', '480p', '360p', '240p']
    aud_res = ['256kbps', '128kbps', '48kbps']

    # If no resolution is provided, choose the highest resolution available
    res_flag = True
    if res == '':
        res_flag = False

    vid_flag = False
    for vi_res in vid_res:
        try:
            if res_flag:
                if vi_res != res:
                    continue
            yt.streams.filter(res=vi_res, only_video=True, progressive=False).first().download(filename=vid_path)
            vid_flag = True
            break
        except (Exception):
            continue

    if not vid_flag:
        print('No suitable video stream found')
        exit(1)

    aud_flag = False
    for au_res in aud_res:
        try:
            yt.streams.filter(abr=au_res, only_audio=True, progressive=False).first().download(filename=aud_path)
            aud_flag = True
        except (Exception):
            continue
    
    if not aud_flag:
        print('No suitable audio stream found')
        exit(1)

    print('Download complete')
    return vid_path, aud_path

def save_video(yt, dest_path, vid_path, aud_path):
    print('Save as: ' + dest_path)
    print('Saving...')
    try:
        video = ffmpeg.input(vid_path)
        audio = ffmpeg.input(aud_path)
        filename = rf'{dest_path}\{clean_filename(yt.title)}.mp4'
        stream = ffmpeg.output(audio, video, filename)
        ffmpeg.run(stream)
        print('Finish')
    except:
        print('Can not save the video')

def main():
    parser = argparse.ArgumentParser(description='YouTube Video Downloader')
    parser.add_argument('dest_path', metavar='dest_path', type=str, help='The destination folder')
    parser.add_argument('link', metavar='link', type=str, help='The link to the YouTube video you want to download')
    parser.add_argument('--res', metavar='res', type=str, required=False, default='', help='The resolution of the YouTube video you want to download')
    args = parser.parse_args()

    dest_path = args.dest_path
    link = args.link
    res = args.res

    yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    vid_path, aud_path = download_video(yt, res)
    save_video(yt, dest_path, vid_path, aud_path)   

if __name__ == '__main__':
    main()