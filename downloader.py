import json, pyperclip, utils
from yt_dlp import YoutubeDL
from playsound3 import playsound
from typing import Callable


abort_requested: bool = False


# Checks if user gave a list of URLs or not. Also if user pressed CANCEL button.
def download(end_thread: Callable[[], None], urls: list[str] | None = None) -> None:
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


# Starts yt-dlp, downloads files and makes an entry into the history.txt if successfull.
def start_yt_dlp(url: str) -> None:
    with open("ydl_config.json", "r", encoding="UTF-8") as config:
        ydl_config = json.load(config)
    try:
        with YoutubeDL(ydl_config) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "Unknown title")
            ydl.download([url])
        utils.log_entry(url, video_title)
        playsound("alert.mp3")

    except Exception:
        playsound("error.mp3")


if __name__ == "__main__":
    pass
