
<h1 align="center">Music Folder Renamer</h1>
<p align="center">
  <img src="https://i.ibb.co/qsbQ8WT/banner.png" alt="MFR Banner"/>
</p>
<!-- ![badge]() -->
<!-- ![badge]() -->
<p align="center">This script will go through all the subfolders in your music folder and rename them to match the album title, year, and record type of the audio files in each folder. This can be useful for organizing your music collection and making it easier to find the songs you're looking for.</p>

Table of Contents
-----------------

-   [Install & Setup](#installsetup)
-   [Usage](#usage)

Background
----------

I made this because I needed to format my music folders, but I have over 6,000 files, so I can't do it manually.


Install & Setup
---------------

This requires mutagen & python.
<br />To install mutagen:
```python
pip install mutagen
```
[Install Python](https://www.python.org/downloads/)

Usage
-----

Open the `format.py` file inside a text/code editor, and change `"C:\path\to\music"` at `line 56` to your music path.
<br />Execute the script by running `py format.py` in CMD, or by opening the .py file.
<br />The format is `{Album} {Year} - {RecordType}`
<br />Your folder structure should look like this for it to work.
``` 
Music/
├─ Artist/
│  ├─ Album/
│  │  ├─ Song.flac/
```
<img src="https://raw.githubusercontent.com/polysymphonic/MusicFolderRenamer/main/example1.gif">
<img src="https://i.ibb.co/3N7W0rf/cmd-Eqx-E8iv-JZe.png">
**I suggest backing up your music before doing this, just incase anything goes wrong.**
