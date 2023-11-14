
# Polysymphonic Music Formatter

<img src="https://i.ibb.co/qsbQ8WT/banner.png">

Organize your music collection by renaming folders and files using customizable formats.

## Features

* Rename folders based on album metadata (artist, album, year, type)
* Rename music files based on track metadata (track number, track title, artist, album artist)
* Customizable naming formats for both folders and files
* Uses placeholder tags to format folders and files
* Supports various audio formats (FLAC, MP3, OGG, M4A, WAV)

## Installation

1. Install Python 3.7 or higher.
2. Install the required Python libraries:
```bash
pip install tkinter ttk mutagen configparser
```

## Usage

1. Run (or open) `formatter.py`.
2. Select the root directory containing your music folders.
3. Enter the desired album format template.
4. Enter the desired song format template.
5. Select the audio format to consider for extracting album information.
6. Click the "Format Albums" button.
<img src="https://raw.githubusercontent.com/polysymphonic/MusicFolderRenamer/main/example.gif">

## Album Format Template

The album format template uses placeholder tags that will be replaced with actual album information:

- `{Album}`: Album title
- `{Artist}`: Album artist
- `{Year}`: Year of release
- `{Type}`: Album type (Album, EP, Single)

## Song Format Template

The song format template uses placeholder tags that will be replaced with actual track information:

- `{TrackNumber}`: Track number
- `{Track}`: Track title
- `{Artist}`: Track artist
- `{AlbumArtist}`: Album artist

## Example Album Format Templates

- `{Album} ({Year})`
- `{Album} ({Artist}) - ({Year})`
- `{Album} - {Artist}`

## Example Song Format Templates

- `{TrackNumber} - {Track}`
- `{TrackNumber} - {Track} - {Artist}`
- `{TrackNumber} - {Track} - {Artist} - {AlbumArtist}`

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
