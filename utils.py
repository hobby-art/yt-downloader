import os, json, datetime


# Function called by "Download history" button.
def open_history() -> None:
    os.startfile("history.txt")


# Function called by "Update yt-dlp" button.
def update_ydl() -> None:
    os.startfile("update_ydl.bat")


# Function used by quality selection combobox, audio_checkbox and setting the default quality after the launch.
def set_quality(selection: str) -> None:

    match selection:
        case "144":
            update_config("format", "best[height<=144]/best")
        case "240":
            update_config("format", "best[height<=240]/best")
        case "360":
            update_config("format", "best[height<=360]/best")
        case "480":
            update_config("format", "best[height<=480]/best")
        case "720":
            update_config("format", "bestvideo[height<=720]+bestaudio/best")
        case "1080":
            update_config("format", "bestvideo[height<=1080]+bestaudio/best")
        case "1440":
            update_config("format", "bestvideo[height<=1440]+bestaudio/best")
        case "2160":
            update_config("format", "bestvideo+bestaudio/best")


# Make an entry in the history.txt file after a successfull download.
def log_entry(url: str, title: str) -> None:
    now = datetime.datetime.today()
    formatted_time = now.strftime("%Y-%m-%d %H:%M")
    with open("history.txt", "a") as file:
        file.write(formatted_time + ", " + '"' + title + '"' + ", " + url + "\n")


# Update ydl_config keys.
def update_config(key, value) -> None:
    file = "ydl_config.json"

    with open(file, "r", encoding="UTF-8") as config_file:
        data = json.load(config_file)

    data[key] = value

    with open(file, "w", encoding="UTF-8") as config_file:
        json.dump(data, config_file, indent=4)


# Get ydl_config option values.
def get_config_value(key: str, default=None) -> str:
    file: str = "ydl_config.json"

    with open(file, "r", encoding="UTF-8") as config_file:
        data = json.load(config_file)

    return data.get(key, default)


# Formats urls from the text field into an array.
def input_check(input: str) -> None | list[str]:
    if not input:
        return
    else:
        urls_list = input.splitlines()
        return urls_list


if __name__ == "__main__":
    pass
