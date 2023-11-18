import os
import re
import string
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter
from PIL import Image

flac_files_found = False
current_theme = "Dark"
theme_button_image = None
root = None


def install_required_packages():
    try:
        with open('requirements.txt', 'r') as file:
            requirements = file.read().splitlines()
    except FileNotFoundError:
        print("requirements.txt not found. Make sure the file exists.")
        return

    for requirement in requirements:
        print(f"Installing {requirement}...")
        subprocess.run(['pip', 'install', requirement])
        print(f"{requirement} installed successfully.")

install_required_packages()

import configparser
from mutagen import File

config_file_path = "config.ini"

if not os.path.exists(config_file_path):
    with open(config_file_path, "w") as configfile:
        configfile.write("[Settings]\n")

configure = configparser.ConfigParser()
configure.read(config_file_path)

root_directory = configure.get("Settings", "RootDirectory", fallback="")
album_format = configure.get("Settings", "AlbumFormat", fallback="{Album} ({Year}) - {Type}")
song_format = configure.get("Settings", "SongFormat", fallback="{TrackNumber} - {Track}")

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
    invalid_chars = set(r'< > : " / \ | ? *'.split())
    return ''.join(c if c not in invalid_chars else '_' for c in name)

def process_folder(folder_path, album_format, song_format, message_label):
    audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.flac')]

    if not audio_files:
        message_label.configure(text="No FLAC files found in the selected directory.", text_color="#FF8080")
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
        message_label.configure(text="Albums formatted successfully!", text_color="#90EE90")
    except Exception as e:
        print(f"Error renaming {folder_path}: {e}")
        message_label.configure(text=f"Error formatting albums: {e}", text_color="#FF8080")

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
        new_song_path = os.path.join(new_folder_path, new_song_name + '.flac')

        try:
            os.rename(old_song_path, new_song_path)
            print(f"Renamed: {old_song_path} -> {new_song_path}")
        except Exception as e:
            print(f"Error renaming {old_song_path}: {e}")

def process_root_folder(root_folder, album_format, song_format, message_label):
    global flac_files_found

    flac_files_found = False

    for root, dirs, files in os.walk(root_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)

            audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.flac')]

            if audio_files:
                flac_files_found = True

                first_audio_file = os.path.join(folder_path, audio_files[0])

                try:
                    audio = File(first_audio_file)
                    album = audio.get('album', [''])[0]
                    date_released = audio.get('date', [''])[0]
                except Exception as e:
                    print(f"Error reading metadata for {first_audio_file}: {e}")
                    continue


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
                except Exception as e:
                    print(f"Error renaming {folder_path}: {e}")

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
                    new_song_path = os.path.join(new_folder_path, new_song_name + '.flac')

                    try:
                        os.rename(old_song_path, new_song_path)
                        print(f"Renamed: {old_song_path} -> {new_song_path}")
                    except Exception as e:
                        print(f"Error renaming {old_song_path}: {e}")

def theme_changer():
    global current_theme, theme_button_image, root
    if current_theme == "Light":
        customtkinter.set_appearance_mode("Dark")
        current_theme = "Dark"
    else:
        customtkinter.set_appearance_mode("Light")
        current_theme = "Light"

    image_path_light = r"img\sun.png"
    image_path_dark = r"img\moon.png"

    theme_button_image = customtkinter.CTkImage(
        Image.open(image_path_light if current_theme == "Dark" else image_path_dark),
        size=(25, 25)
    )

    root.lone_button.configure(image=theme_button_image)

    root.lone_button.configure(image=theme_button_image)

def format_albums_and_songs():
    global entry_root_dir, entry_album_format, entry_song_format, root_directory, album_format, message_label, flac_files_found

    message_label.configure(text="")

    root_dir = entry_root_dir.get()
    album_format = entry_album_format.get()
    song_format = entry_song_format.get()

    if root_dir and album_format:
        if not configure.has_section("Settings"):
            configure.add_section("Settings")

        configure.set("Settings", "RootDirectory", root_dir)
        configure.set("Settings", "AlbumFormat", album_format)
        configure.set("Settings", "SongFormat", song_format)
        with open(config_file_path, "w") as configfile:
            configure.write(configfile)

        process_root_folder(root_dir, album_format, song_format, message_label)

        if flac_files_found:
            message_label.configure(text="Formatted albums!", text_color="#90EE90")
        else:
            message_label.configure(text="Could not find FLACs", text_color="#FF8080")


def select_root_directory():
    global entry_root_dir, root_directory

    root_dir = filedialog.askdirectory(initialdir=root_directory, title="Select Root Directory")
    if root_dir:
        entry_root_dir.delete(0, tk.END)
        entry_root_dir.insert(0, root_dir)
        root_directory = root_dir

def create_gui():
    global theme_button_image, root

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")
    global entry_root_dir, entry_album_format, entry_song_format, root_directory, album_format, message_label

    root = customtkinter.CTk()
    root.title("Music Formatter")
    root.geometry("390x245")
    root.resizable(True, True)

    label_root_dir = customtkinter.CTkLabel(root, text="Music Folder", fg_color="transparent")
    label_root_dir.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_root_dir = customtkinter.CTkEntry(root, width=190, placeholder_text="miau miau")
    entry_root_dir.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    entry_root_dir.insert(0, root_directory)

    button_select = customtkinter.CTkButton(root, width=75, text="Browse", command=select_root_directory)
    button_select.grid(row=0, column=2, padx=0, pady=0, sticky="w")

    label_album_format = customtkinter.CTkLabel(root, text="Album Format", fg_color="transparent")
    label_album_format.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    entry_album_format = customtkinter.CTkEntry(root, width=190, placeholder_text="miau miau")
    entry_album_format.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    entry_album_format.insert(0, album_format)

    label_song_format = customtkinter.CTkLabel(root, text="Song Format", fg_color="transparent")
    label_song_format.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    entry_song_format = customtkinter.CTkEntry(root, width=190, placeholder_text="miau miau")
    entry_song_format.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    entry_song_format.insert(0, song_format)

    button = customtkinter.CTkButton(master=root, text="Format Albums", command=format_albums_and_songs)
    button.grid(row=3, column=0, columnspan=3, pady=10)

    message_label = customtkinter.CTkLabel(root, text="", fg_color="transparent")
    message_label.grid(row=4, column=0, columnspan=3, pady=10)
    
    image_path_light = r"img\sun.png"
    image_path_dark = r"img\moon.png"

    theme_button_image = customtkinter.CTkImage(
        Image.open(image_path_light if current_theme == "Dark" else image_path_dark),
        size=(25, 25)
    )

    root.lone_button = customtkinter.CTkButton(
        master=root, text="", width=30, image=theme_button_image, command=theme_changer
    )
    root.lone_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="sw")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
