import downloader, threading, utils
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


## FUNCTIONS


# Function called by DOWNLOAD button.
def start_download_thread() -> None:

    # Changing the state of DOWNLOAD button, to CANCEL button.
    download_button["text"] = "\nCANCEL\n"
    download_button["command"] = abort

    # Reset counters for the donwload qeue
    global qeue
    qeue = 0
    global counter
    counter = 0

    # Validate text field input.
    text: str | None = input_field.get("1.0", "end-1c")
    urls: list[str] | None = None
    if text:
        urls = utils.input_check(text)
        initialize_counter(len(urls))
    else:
        initialize_counter(1)

    # Start a new thread for download process.
    thread = threading.Thread(
        target=downloader.download,
        args=(end_download_thread, update_text_field, update_counter, urls),
    )
    thread.daemon = True
    thread.start()


# Receiving callback function after finishing downloading.
# After finish - enable DOWNLOAD button.
def end_download_thread() -> None:
    window.after(0, enable_download_button)


# Callback that gets text information from yt-dlp
def update_text_field(data) -> None:
    input_field.delete("1.0", "end")
    input_field.insert("1.0", data)


# Global variables for the counter
qeue = 0
counter = 0


# Print the number of videos that are qeued for download
def initialize_counter(sum):
    global qeue
    qeue = sum
    label_counter_var.set(f"0/{qeue}")


# Callback to receive postprocessor hooks to update the counter
def update_counter(hook):
    global counter
    if hook.get("postprocessor") == "MoveFiles" and hook.get("status") == "finished":
        counter += 1
        label_counter_var.set(f"{counter}/{qeue}")


# Change the CANCEL button back into DOWNLOAD button.
def enable_download_button() -> None:
    download_button["text"] = "\nDOWNLOAD\n"
    download_button["command"] = start_download_thread
    input_field["state"] = "normal"


# Function called if CANCEL button pressed.
def abort() -> None:
    downloader.abort_requested = True
    download_button["text"] = "\nDOWNLOAD\n"
    download_button["command"] = start_download_thread
    input_field["state"] = "normal"


# Function called when the checkbox "Audio only" pressed.
def audio_checkbox() -> None:
    current_quality = quality_selection_combobox.get()
    if is_only_audio.get():
        quality_selection_combobox["state"] = "disabled"
        utils.update_config("format", "bestaudio/best")
    else:
        quality_selection_combobox["state"] = "enabled"
        utils.set_quality(current_quality)
        selected_quality.set(current_quality)


# Function called by "Choose folder" button.
def select_folder() -> None:
    selected_folder = filedialog.askdirectory()
    if select_folder:
        folder_var.set(selected_folder)
        save_path = selected_folder + "/%(title)s.%(ext)s"
        utils.update_config("outtmpl", save_path)


## GUI

# Main window
window = tk.Tk()
window.title("YT-DOWNLOADER")
window.geometry("700x450")


# Lables frame for: instructions label, counter label.
text_frame = ttk.Frame(window)

# Label with instructions.
label_instructions = ttk.Label(
    window,
    text="If the text field is empty, URL will be taked from the clipboard.\nOtherwise, you can paste several URLs separated by a new line.",
    font="Calibri 12",
)

# Counter label
label_counter_var = tk.StringVar(value="0/0")
label_counter = ttk.Label(window, textvariable=label_counter_var, font="Calibri 12")

# Text frame positioning
label_instructions.pack()
label_counter.pack()

label_instructions.pack_propagate(False)
label_instructions.pack()

# Text field for URLs input.
input_field = tk.Text(window, height=10)
input_field.pack(side="top")


# Top frame for: download button, quality selection, audio only checkbox.
top_frame = ttk.Frame(window, width=650, height=80, borderwidth=10, relief=tk.GROOVE)

# Download button
download_button = ttk.Button(
    top_frame,
    text="\nDOWNLOAD\n",
    width=25,
    command=start_download_thread,
)

# Quality selection
quality_options: tuple[str, ...] = (
    "144",
    "240",
    "360",
    "480",
    "720",
    "1080",
    "1440",
    "2160",
)

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
    command=audio_checkbox,
)

# Top_frame positioning
download_button.pack(side="left")
quality_selection_combobox.pack(side="left", pady=15, padx=100)
audio_only_checkbox.pack(side="left")

top_frame.pack_propagate(False)
top_frame.pack(pady=10)


# Middle frame for: choose save path button, show selected path label.
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

# Show selected folder label
path_label = ttk.Label(middle_frame, textvariable=folder_var)

# Middle frame positioning
path_button.pack(side="left")
path_label.pack(side="left", padx=50)

middle_frame.pack_propagate(False)
middle_frame.pack()


# Bottom frame for: "Download history" button, "Update yt-dlp" button
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
