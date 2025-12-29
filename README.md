# term-paint

## Description

This is a CLI tool for drawing images in your terminal with keyboard controls. For wide compatibility, only 8 terminal colors are used - an image that uses different colors will round them to the nearest supported color when loaded and saved.

## Usage

- E to toggle drawing mode (`X` in infobar means drawing is disabled; `%` in infobar means it is enabled)
- W,A,S,D to move around the image
- 1...7 for switching colors (indicated on the left of the infobar)
- 0 to switch to black (default fill color)
- B to show a view of the image in your default image viewer
- X to save the image under the filename provided (nameless files are saved as `unnamed.png`)
- Q to exit the program without saving any changes

## Installation

From [PyPI](https://pypi.org/project/term-paint/):

- `pip install term-paint` or `pipx install term-paint` or `uvx install term-paint`
- `term-paint [OPTIONS]`

From wheel files:

- Download the wheel files from the release and place them into a new directory
- `uv install .`
- `term-paint [OPTIONS]`

From the repo:

- `git clone https://github.com/strawberry-p/term-paint.git`
- `cd term-paint`
- `py paint.py [OPTIONS]`