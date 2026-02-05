import json, pyperclip, utils
from yt_dlp import YoutubeDL
from playsound3 import playsound
from typing import Callable
import traceback


abort_requested: bool = False


# Checks if user gave a list of URLs or not. Also if user pressed CANCEL button.
def download(
    end_thread: Callable[[], None],
    callback_update_text,
    update_counter,
    urls: list[str] | None = None,
) -> None:

    global abort_requested
    abort_requested = False

    ydl_config = config_preparation(callback_update_text, update_counter)

    if not urls:
        url = pyperclip.paste()
        start_yt_dlp(url, ydl_config)
    else:
        for url in urls:
            if abort_requested:
                break
            start_yt_dlp(url, ydl_config)
    end_thread()


# Read the config, add Logger and return it.
def config_preparation(callback_update_text, update_counter) -> dict:
    with open("ydl_config.json", "r", encoding="UTF-8") as config:
        ydl_config = json.load(config)
        ydl_config["logger"] = MyLogger(callback_update_text)
        ydl_config["postprocessor_hooks"] = [lambda hook: update_counter(hook)]
        return ydl_config


# Starts yt-dlp and makes an entry into the history.txt if successfull.
def start_yt_dlp(url: str, ydl_config) -> None:
    try:
        with YoutubeDL(ydl_config) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "Unknown title")
            ydl.download([url])
        utils.log_entry(url, video_title)
        playsound("alert.mp3")
    except Exception:
        playsound("error.mp3")


# yg-dlp logger to sent log information to the GUI via callback function
class MyLogger:
    def __init__(self, ui_callback):
        self.ui_callback = ui_callback

    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            pass
        else:
            self.info(msg)
            self.ui_callback(msg)

    def info(self, msg):
        self.ui_callback(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        self.ui_callback(msg)


if __name__ == "__main__":
    pass
