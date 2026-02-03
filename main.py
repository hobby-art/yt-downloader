import downloader, threading, utils
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# Functions
def disable_quality_selection():
    current_quality = quality_selection_combobox.get()
    if is_only_audio.get():
        quality_selection_combobox["state"] = "disabled"
        utils.update_config("format", "bestaudio/best")
    else:
        quality_selection_combobox["state"] = "enabled"
        utils.set_quality(current_quality)
        selected_quality.set(current_quality)


def select_folder():
    selected_folder = filedialog.askdirectory()
    if select_folder:
        folder_var.set(selected_folder)
        save_path = selected_folder + "/%(title)s.%(ext)s"
        utils.update_config("outtmpl", save_path)


def start_download_thread():
    download_button["text"] = "\nCANCEL\n"
    download_button["command"] = abort

    input_field["state"] = "disabled"

    text = input_field.get("1.0", "end-1c")
    urls = utils.input_check(text)
    thread = threading.Thread(
        target=downloader.download, args=(end_download_thread, urls)
    )
    thread.daemon = True
    thread.start()


def end_download_thread():
    window.after(0, enable_download_button)


def enable_download_button():
    download_button["text"] = "\nDOWNLOAD\n"
    download_button["command"] = start_download_thread
    input_field["state"] = "normal"


def abort():
    downloader.abort_requested = True
    download_button["text"] = "\nDOWNLOAD\n"
    download_button["command"] = start_download_thread
    input_field["state"] = "normal"


# Main window
window = tk.Tk()
window.title("YT-DOWNLOADER")
window.geometry("700x450")

# Instructions label
label_instructions = ttk.Label(
    master=window,
    text="If the text field is empty, URL will be taked from the clipboard.\nOtherwise, you can paste several URLs separated by a new line.",
    font="Calibri 15",
)
label_instructions.pack()

# Text field
input_field = tk.Text(window, height=10)
input_field.pack()

# Top frame: download button, quality selection, audio only checkbox
top_frame = ttk.Frame(window, width=650, height=80, borderwidth=10, relief=tk.GROOVE)

# Download button
download_button = ttk.Button(
    top_frame,
    text="\nDOWNLOAD\n",
    width=25,
    command=start_download_thread,
)

# Quality selection
quality_options = ("144", "240", "360", "480", "720", "1080", "1440", "2160")

selected_quality = tk.StringVar(value="1080")
quality_selection_combobox = ttk.Combobox(
    top_frame, values=quality_options, textvariable=selected_quality
)
quality_selection_combobox.bind(
    "<<ComboboxSelected>>",
    lambda _: utils.set_quality(quality_selection_combobox.get()),
)

# Audio only checkbox
is_only_audio = tk.BooleanVar(value=False)
audio_only_checkbox = ttk.Checkbutton(
    top_frame,
    text="Audio only",
    variable=is_only_audio,
    command=disable_quality_selection,
)

# Top_frame positioning
download_button.pack(side="left")
quality_selection_combobox.pack(side="left", pady=15, padx=100)
audio_only_checkbox.pack(side="left")

top_frame.pack_propagate(False)
top_frame.pack(pady=10)

# Middle frame: choose save path button, show selected path.
middle_frame = ttk.Frame(window, width=650, height=50, borderwidth=10, relief=tk.GROOVE)

# Select save folder button
folder_var = tk.StringVar(
    value=utils.get_config_value(
        "outtmpl", "Selected folder - current working directory"
    )
)
path_button = ttk.Button(
    middle_frame,
    text="Choose folder",
    command=select_folder,
)

# Show selected folder
path_label = ttk.Label(middle_frame, textvariable=folder_var)


# Middle frame positioning
path_button.pack(side="left")
path_label.pack(side="left", padx=50)

middle_frame.pack_propagate(False)
middle_frame.pack()

# Bottom frame
bottom_frame = ttk.Frame(window, width=650, height=50, borderwidth=10, relief=tk.GROOVE)

# History button
history_button = ttk.Button(
    bottom_frame, text="Download history", command=utils.open_history
)

# Update yt-dlp button
update_dlp_button = ttk.Button(
    bottom_frame, text="Update yt-dlp", command=utils.update_ydl
)

# Bottom frame positioning
history_button.pack(side="left")
update_dlp_button.pack(side="right")

bottom_frame.pack_propagate(False)
bottom_frame.pack(pady=10)

# Set defaults and start the mainloop
utils.set_quality("1080")
window.mainloop()
