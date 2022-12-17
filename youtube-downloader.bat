@echo off
set dest_dir=" -the directory where the video will be downloaded to-"
cd /d " -the directory of the python file- "
python yt_downloader.py %dest_dir% %1