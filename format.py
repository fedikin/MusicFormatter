import os
import re
import string
import tkinter as tk
from tkinter import ttk, filedialog

try:
    import configparser
    print("ConfigParser already installed.")
except ImportError:
    print("ConfigParser not installed. Installing now...")
    os.system("pip install configparser==5.0.2")
    import configparser

try:
    from mutagen import File
    print("Mutagen already installed.")
except ImportError:
    print("Mutagen not installed. Installing now...")
    os.system("pip install mutagen==1.45.1")
    from mutagen import File

config_file_path = "config.ini"

if not os.path.exists(config_file_path):
    with open(config_file_path, "w") as configfile:
        configfile.write("[Settings]\n")

config = configparser.ConfigParser()
config.read(config_file_path)

root_directory = config.get("Settings", "RootDirectory", fallback="")
album_format = config.get("Settings", "AlbumFormat", fallback="{Album} ({Year}) - {Type}")
audio_format = config.get("Settings", "AudioFormat", fallback="flac")
song_format = config.get("Settings", "SongFormat", fallback="{TrackNumber} - {Track}")

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
        audio = File(file_path)
        artist = audio.get('artist', [''])[0]
        album_artist = audio.get('albumartist', [''])[0]
        return artist, album_artist
    except Exception as e:
        print(f"Error reading artist metadata for {file_path}: {e}")
        return "", ""

def replace_invalid_characters(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c if c in valid_chars else '_' for c in name)

def process_folder(folder_path, album_format, audio_format, song_format, message_label):
    audio_files = [f for f in os.listdir(folder_path) if f.endswith(f'.{audio_format}')]

    if not audio_files:
        message_label.config(text=f"No {audio_format} files found in the selected directory.", fg="red")
        return

    first_audio_file = os.path.join(folder_path, audio_files[0])

    try:
        audio = File(first_audio_file)
        album = audio.get('album', [''])[0]
        date_released = audio.get('date', [''])[0]
    except Exception as e:
        print(f"Error reading metadata for {first_audio_file}: {e}")
        return

    folder_type = get_folder_type(len(audio_files))
    year = get_year_from_date(date_released)

    if '{Artist}' in album_format:
        artist, _ = get_artist_from_file(first_audio_file)
        album_format = album_format.replace('{Artist}', artist)

    new_folder_name = replace_invalid_characters(album_format.format(Album=album, Year=year, Type=folder_type))
    new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

    try:
        os.rename(folder_path, new_folder_path)
        print(f"Renamed: {folder_path} -> {new_folder_path}")
        message_label.config(text=f"Albums formatted successfully!", fg="green")
    except Exception as e:
        print(f"Error renaming {folder_path}: {e}")
        message_label.config(text=f"Error formatting albums: {e}", fg="red")

    for audio_file in audio_files:
        old_song_path = os.path.join(new_folder_path, audio_file)
        audio = File(old_song_path)
        track_number = audio.get('tracknumber', [''])[0]
        track = audio.get('title', [''])[0]
        artist, album_artist = get_artist_from_file(old_song_path)

        new_song_name = replace_invalid_characters(song_format.format(
            TrackNumber=str(track_number).zfill(2),
            Track=track,
            Artist=artist,
            AlbumArtist=album_artist
        ))
        new_song_path = os.path.join(new_folder_path, new_song_name + f'.{audio_format}')

        try:
            os.rename(old_song_path, new_song_path)
            print(f"Renamed: {old_song_path} -> {new_song_path}")
        except Exception as e:
            print(f"Error renaming {old_song_path}: {e}")

def process_root_folder(root_folder, album_format, audio_format, song_format, message_label):
    for root, dirs, files in os.walk(root_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            process_folder(folder_path, album_format, audio_format, song_format, message_label)

            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)
                if os.path.isdir(subfolder_path):
                    process_folder(subfolder_path, album_format, audio_format, song_format, message_label)

def format_albums_and_songs():
    global entry_root_dir, entry_album_format, entry_song_format, root_directory, album_format, audio_format_var, song_format_var, message_label

    message_label.config(text="", fg="black")

    root_dir = entry_root_dir.get()
    album_format = entry_album_format.get()
    audio_format = audio_format_var.get()
    song_format = entry_song_format.get()

    if root_dir and album_format and audio_format:
        if not config.has_section("Settings"):
            config.add_section("Settings")

        config.set("Settings", "RootDirectory", root_dir)
        config.set("Settings", "AlbumFormat", album_format)
        config.set("Settings", "AudioFormat", audio_format)
        config.set("Settings", "SongFormat", song_format)
        with open(config_file_path, "w") as configfile:
            config.write(configfile)

        process_root_folder(root_dir, album_format, audio_format, song_format, message_label)

def select_root_directory():
    global entry_root_dir, root_directory

    root_dir = filedialog.askdirectory(initialdir=root_directory)
    if root_dir:
        entry_root_dir.delete(0, tk.END)
        entry_root_dir.insert(0, root_dir)
        root_directory = root_dir

def create_gui():
    global entry_root_dir, entry_album_format, entry_song_format, root_directory, album_format, audio_format_var, song_format_var, message_label

    root = tk.Tk()
    root.title("Music Formatter")
    root.geometry("400x275")
    root.config(bg="#2E2E2E")
    root.resizable(True, True)

    label_root_dir = tk.Label(root, text="Music Folder:", fg="white", bg="#2E2E2E")
    label_root_dir.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_root_dir = tk.Entry(root, width=30)
    entry_root_dir.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    entry_root_dir.insert(0, root_directory)

    button_select = tk.Button(root, text="Browse", command=select_root_directory, fg="#2E2E2E", bg="white")
    button_select.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    label_album_format = tk.Label(root, text="Album Format:", fg="white", bg="#2E2E2E")
    label_album_format.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    entry_album_format = tk.Entry(root, width=30)
    entry_album_format.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    entry_album_format.insert(0, album_format)

    label_song_format = tk.Label(root, text="Song Format:", fg="white", bg="#2E2E2E")
    label_song_format.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    entry_song_format = tk.Entry(root, width=30)
    entry_song_format.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    entry_song_format.insert(0, song_format)

    label_audio_format = tk.Label(root, text="Audio Format:", fg="white", bg="#2E2E2E")
    label_audio_format.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    audio_formats = ["flac", "mp3", "ogg", "m4a", "wav"]
    audio_format_var = tk.StringVar(root)
    audio_format_var.set(audio_format)

    dropdown_audio_format = ttk.Combobox(root, textvariable=audio_format_var, values=audio_formats, state="readonly")
    dropdown_audio_format.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    button_process = tk.Button(root, text="Format Albums", command=format_albums_and_songs, fg="#2E2E2E", bg="white")
    button_process.grid(row=4, column=0, columnspan=3, pady=10)

    message_label = tk.Label(root, text="", fg="black", bg="#2E2E2E")
    message_label.grid(row=5, column=0, columnspan=3, pady=10)

    polysymphonic_label = tk.Label(root, text="polysymphonic", fg="gray", bg="#2E2E2E")
    polysymphonic_label.grid(row=6, column=2, padx=5, pady=0, sticky="se")

    root.mainloop()

if __name__ == "__main__":
    create_gui()

