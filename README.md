# emote-resize
Python script with a GUI that focuses on resizing Twitch.tv emotes.

![Screenshot](https://imgur.com/k2OY1XC.png)

## Features
* Creates a resized image at 50% and 25% of original width and height using the following filters:
  * Nearest Neighbor
  * Box
  * Bilinear
  * Hamming
  * Bicubic
  * Lanczos
* Optionally, packages the output into a zip file.

## Install
Check [latest release](https://github.com/whuppo/emote-resize/releases).

## Requirements
*required versions may be inaccurate*
* Python 3.5.x
* Pillow 7.x

## Building
`pip install pyinstaller`

`pyinstaller resize.spec`

Doing this in a fresh venv might have the module finder not include more than required.