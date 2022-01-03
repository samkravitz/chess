# fen
# License: MIT
# See LICENSE for full license text
# Author: Sam Kravitz
#
# FILE: fen.py
# DATE: January 3rd, 2022
# Description: Converts FEN string to a .png representation of the position
#
# I used this command to batch convert .svg to .png:
# for i in *.svg; do inkscape -w 128 -h 128 --export-png-color-mode=RGBA_16 "$i" -o "${i%.svg}.png"; done
#
# https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

import sys
from PIL import Image

if len(sys.argv) != 2:
    print('Usage: ./fen [FEN string]')
    exit()

image = Image.open('assets/board.png')
bishop = Image.open('assets/bishop-black.png')
image.paste(bishop, (0, 0), mask=bishop)
image.save('output.png')
bishop.close()
image.close()

