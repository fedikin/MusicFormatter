import os
import re
import tkinter as tk
from tkinter import ttk, filedialog

# Check and install configparser
try:
    import configparser
    print("ConfigParser already installed.")
except ImportError:
    print("ConfigParser not installed. Installing now...")
    os.system("pip install configparser==5.0.2")
    import configparser

# Check and install mutagen
try:
    from mutagen.flac import FLAC
    print("Mutagen already installed.")
except ImportError:
    print("Mutagen not installed. Installing now...")
    os.system("pip install mutagen==1.45.1")
    from mutagen.flac import FLAC

# Config file path
config_file_path = "config.ini"

# Check if config.ini exists, create it if not
if not os.path.exists(config_file_path):
    with open(config_file_path, "w") as configfile:
        configfile.write("[Settings]\n")

# Load config
config = configparser.ConfigParser()
config.read(config_file_path)

# Set default values if not present in the config file
root_directory = config.get("Settings", "RootDirectory", fallback="")
album_format = config.get("Settings", "AlbumFormat", fallback="{Album} ({Year}) - {Type}")
audio_format = config.get("Settings", "AudioFormat", fallback="flac")

def get_folder_type(file_count):
    if file_count > 5:
        return "Album"
    elif file_count > 1:
        return "EP"
    else:
        return "Single"

def get_year_from_date(date):
    match = re.search(r'\b(\d{4})\b', date)
    if match:
        return match.group(1)
    else:
        return ""

def get_artist_from_file(file_path):
    try:
        audio = FLAC(file_path)
        artist = audio.get('artist', [''])[0]
        return artist
    except Exception as e:
        print(f"Error reading artist metadata for {file_path}: {e}")
        return ""

def process_folder(folder_path, album_format, audio_format, message_label):
    audio_files = [f for f in os.listdir(folder_path) if f.endswith(f'.{audio_format}')]

    if not audio_files:
        message_label.config(text=f"No {audio_format} files found in the selected directory.", fg="red")
        return

    first_audio_file = os.path.join(folder_path, audio_files[0])

    try:
        audio = FLAC(first_audio_file)
        album = audio.get('album', [''])[0]
        date_released = audio.get('date', [''])[0]
    except Exception as e:
        print(f"Error reading metadata for {first_audio_file}: {e}")
        return

    folder_type = get_folder_type(len(audio_files))
    year = get_year_from_date(date_released)

    if '{Artist}' in album_format:
        artist = get_artist_from_file(first_audio_file)
        album_format = album_format.replace('{Artist}', artist)

    new_folder_name = album_format.format(Album=album, Year=year, Type=folder_type)

    new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

    try:
        os.rename(folder_path, new_folder_path)
        print(f"Renamed: {folder_path} -> {new_folder_path}")
        message_label.config(text=f"Albums formatted successfully!", fg="green")
    except Exception as e:
        print(f"Error renaming {folder_path}: {e}")
        message_label.config(text=f"Error formatting albums: {e}", fg="red")

def process_root_folder(root_folder, album_format, audio_format, message_label):
    for root, dirs, files in os.walk(root_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            process_folder(folder_path, album_format, audio_format, message_label)

            # Now iterate through the subdirectories of the current directory
            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)
                if os.path.isdir(subfolder_path):
                    process_folder(subfolder_path, album_format, audio_format, message_label)

def format_albums():
    global entry_root_dir, entry_album_format, root_directory, album_format, audio_format_var, message_label

    message_label.config(text="", fg="black")  # Clear previous messages

    root_dir = entry_root_dir.get()
    album_format = entry_album_format.get()
    audio_format = audio_format_var.get()

    if root_dir and album_format and audio_format:
        # Check if the 'Settings' section exists, create it if not
        if not config.has_section("Settings"):
            config.add_section("Settings")

        # Save the selected values to the config file
        config.set("Settings", "RootDirectory", root_dir)
        config.set("Settings", "AlbumFormat", album_format)
        config.set("Settings", "AudioFormat", audio_format)
        with open(config_file_path, "w") as configfile:
            config.write(configfile)

        # Format albums using the updated values
        process_root_folder(root_dir, album_format, audio_format, message_label)

def select_root_directory():
    global entry_root_dir, root_directory

    root_dir = filedialog.askdirectory(initialdir=root_directory)
    if root_dir:
        entry_root_dir.delete(0, tk.END)
        entry_root_dir.insert(0, root_dir)
        root_directory = root_dir  # Update the root_directory variable

def create_gui():
    global entry_root_dir, entry_album_format, root_directory, album_format, audio_format_var, message_label

    # Create the main window
    root = tk.Tk()
    root.title("Music Folder Formatter")
    root.geometry("400x230")  # Larger height
    root.config(bg="#2E2E2E")  # Set background color to a semi-dark color
    root.resizable(False, False)  # Make the window not resizable

    # Create and place widgets
    label_root_dir = tk.Label(root, text="Music Folder:", fg="white", bg="#2E2E2E")
    label_root_dir.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_root_dir = tk.Entry(root, width=30)
    entry_root_dir.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    entry_root_dir.insert(0, root_directory)  # Set default value

    button_select = tk.Button(root, text="Browse", command=select_root_directory, fg="#2E2E2E", bg="white")
    button_select.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    label_album_format = tk.Label(root, text="Album Format:", fg="white", bg="#2E2E2E")
    label_album_format.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    entry_album_format = tk.Entry(root, width=30)
    entry_album_format.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    entry_album_format.insert(0, album_format)  # Set default value

    label_audio_format = tk.Label(root, text="Audio Format:", fg="white", bg="#2E2E2E")
    label_audio_format.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    audio_formats = ["flac", "mp3", "ogg", "m4a", "wav"]  # Add more formats as needed
    audio_format_var = tk.StringVar(root)
    audio_format_var.set(audio_format)  # Set default value

    # Use ttk.Combobox for a better-looking dropdown
    dropdown_audio_format = ttk.Combobox(root, textvariable=audio_format_var, values=audio_formats, state="readonly")
    dropdown_audio_format.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    button_process = tk.Button(root, text="Format Albums", command=format_albums, fg="#2E2E2E", bg="white")
    button_process.grid(row=3, column=0, columnspan=3, pady=10)

    # Message label to display status messages
    message_label = tk.Label(root, text="", fg="black", bg="#2E2E2E")
    message_label.grid(row=4, column=0, columnspan=3, pady=10)
    
    polysymphonic_label = tk.Label(root, text="polysymphonic", fg="gray", bg="#2E2E2E")
    polysymphonic_label.grid(row=5, column=2, padx=5, pady=0, sticky="se")  # Place it in the bottom right corner
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()

