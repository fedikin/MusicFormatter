import os
import re
from mutagen.flac import FLAC

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

def process_folder(folder_path):
    flac_files = [f for f in os.listdir(folder_path) if f.endswith('.flac')]

    if not flac_files:
        return

    first_flac_file = os.path.join(folder_path, flac_files[0])

    try:
        audio = FLAC(first_flac_file)
        album = audio.get('album', [''])[0]
        date_released = audio.get('date', [''])[0]
    except Exception as e:
        print(f"Error reading metadata for {first_flac_file}: {e}")
        return

    folder_type = get_folder_type(len(flac_files))
    year = get_year_from_date(date_released)

    new_folder_name = f"{album} ({year}) - {folder_type}"

    new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

    try:
        os.rename(folder_path, new_folder_path)
        print(f"Renamed: {folder_path} -> {new_folder_path}")
    except Exception as e:
        print(f"Error renaming {folder_path}: {e}")

def process_root_folder(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            process_folder(folder_path)

if __name__ == "__main__":
    root_directory = r"C:\path\to\music"
    process_root_folder(root_directory)
