import os, json, datetime


def open_history():
    os.startfile("history.txt")


def update_ydl():
    os.startfile("update_ydl.bat")


def set_quality(selection):

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


def log_entry(url, title):
    now = datetime.datetime.today()
    formatted_time = now.strftime("%Y-%m-%d %H:%M")
    with open("history.txt", "a") as file:
        file.write(formatted_time + ", " + '"' + title + '"' + ", " + url + "\n")


def update_config(key, value):
    file = "ydl_config.json"

    with open(file, "r", encoding="UTF-8") as config_file:
        data = json.load(config_file)

    data[key] = value

    with open(file, "w", encoding="UTF-8") as config_file:
        json.dump(data, config_file, indent=4)


def get_config_value(key, default=None):
    file = "ydl_config.json"

    with open(file, "r", encoding="UTF-8") as config_file:
        data = json.load(config_file)

    return data.get(key, default)


def input_check(input):
    if input == "":
        return
    else:
        urls_list = input.splitlines()
        return urls_list


if __name__ == "__main__":
    pass
