
Music Folder Renamer
=============
<p align="center"![banner](https://i.ibb.co/qsbQ8WT/banner.png)</p>
<!-- ![badge]() -->
<!-- ![badge]() -->
This takes your music folder, goes through all the sub-folders and changes the folder names based on the metadata, using mutagen & python.

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
<br /><br />**I suggest backing up your music before doing this, just incase anything goes wrong.**
