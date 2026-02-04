# Video Downloader 🎥
A simple Python tool to download videos using `yt-dlp`.

## Setup Instructions
1.	Install python (project written in 3.14.2). During installation check the box "Add Python to PATH".
2.	Download ffmpeg. For example, here: https://www.gyan.dev/ffmpeg/builds/. Look for the "Essentials" or "Full" zip.
3.	Extract ffmpeg.exe and ffprobe.exe from the bin folder of the zip and drop them into the project folder.
4.	In the project folder run start.bat. If you don’t have venv, it will create one and install dependencies from requirements.txt.

## How to use it
Select a folder where to save files. If none selected, the program may give an error.

If you need to download only one video (or audio), just copy the link and press DOWNLOAD. The program will take the link from the clipboard.

To download several videos, put their links in the text field separated by a new line.

If a video doesn’t have selected quality, the best available will be used. Format – mp4.

Audio files are downloaded in the best available audio format.

CANCEL button doesn’t stop the current download, only the following.

Yt-dlp can have updates to work correctly, so if you get errors, try to update it by pressing “Update yt-dlp”

If you want to change or add yt-dlp options, you can do that in 'ydl_config.json' file.
