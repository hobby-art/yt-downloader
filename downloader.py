import json, pyperclip, utils
from yt_dlp import YoutubeDL
from playsound3 import playsound


abort_requested = False


def download(end_thread, urls=[]):
    global abort_requested
    abort_requested = False
    if not urls:
        url = pyperclip.paste()
        start_yt_dlp(url)
    else:
        for url in urls:
            if abort_requested:
                break
            start_yt_dlp(url)
    end_thread()


def start_yt_dlp(url: str):
    with open("ydl_config.json", "r", encoding="UTF-8") as config:
        ydl_config = json.load(config)
    try:
        with YoutubeDL(ydl_config) as ydl:  # type: ignore
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "Unknown title")
            ydl.download([url])
        utils.log_entry(url, video_title)
        playsound("alert.mp3")

    except Exception:
        playsound("error.mp3")


if __name__ == "__main__":
    pass
