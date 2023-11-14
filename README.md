# Folder Formatter

<img src="https://i.ibb.co/qsbQ8WT/banner.png">

Organize your music collection by renaming folders to a consistent album format.

## Features

* Rename folders based on album information extracted from audio files.
* Customizable album format template.
* Supports multiple audio formats (FLAC, MP3, OGG, M4A, WAV).
* Automatically scans subdirectories for music files.

## Installation

1. Install Python 3.7 or higher.
2. Install the required Python libraries:
   ```bash
   pip install tkinter ttk mutagen configparser
   ```

## Usage

1. Run the script `album_formatter.py`.
2. Select the root directory containing your music folders.
3. Enter the desired album format template.
4. Select the audio format to consider for extracting album information.
5. Click the "Format Albums" button.
<img src="https://raw.githubusercontent.com/polysymphonic/MusicFolderRenamer/main/example1.gif">

## Album Format Template

The album format template uses placeholder tags that will be replaced with actual album information:

- `{Album}`: Album title
- `{Artist}`: Artist name
- `{Year}`: Year of release
- `{Type}`: Album type (Album, EP, Single)

## Example Album Format Templates

- `{Album} ({Year})`
- `{Album} ({Artist}) - ({Year})`
- `{Album} - {Artist}`

## Supported Audio Formats

The script currently supports the following audio formats:

- FLAC (.flac)
- MP3 (.mp3)
- OGG (.ogg)
- M4A (.m4a)
- WAV (.wav)

## Contributing

Feel free to contribute to this project by submitting bug reports, feature requests, or pull requests.

## License

This project is licensed under the MIT License.
