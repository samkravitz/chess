#! /usr/bin/python

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
from datetime import datetime
from PIL import Image

sections = []

if len(sys.argv) == 2:
    fen = sys.argv[1]
    sections = fen.split(" ")
elif len(sys.argv) == 7:
    sections = sys.argv[1:]
else:
    print('Usage: ./fen [FEN string]')
    exit()

image = Image.open('assets/board.png')
rank = 1
file = 1    # h

# there are 6 sections in a valid FEN string
if len(sections) != 6:
    print('Error: invalid FEN')
    exit()

def get_piece(char):
    filepath = ''
    match char:
        case 'p':
          filepath = 'assets/pawn-black.png'
        case 'n':
          filepath = 'assets/knight-black.png'
        case 'b':
          filepath = 'assets/bishop-black.png'
        case 'r':
          filepath = 'assets/rook-black.png'
        case 'q':
          filepath = 'assets/queen-black.png'
        case 'k':
          filepath = 'assets/king-black.png'
        case 'P':
          filepath = 'assets/pawn-white.png'
        case 'N':
          filepath = 'assets/knight-white.png'
        case 'B':
          filepath = 'assets/bishop-white.png'
        case 'R':
          filepath = 'assets/rook-white.png'
        case 'Q':
          filepath = 'assets/queen-white.png'
        case 'K':
          filepath = 'assets/king-white.png'


    if filepath == '':
        print('Error: invalid FEN')
        exit()
    
    piece = Image.open(filepath)
    if piece is None:
        print('Error: invalid FEN')
        exit()

    return piece

def get_offset(rank, file):
    PIECE_WIDTH = PIECE_HEIGHT = 128
    rank -= 1
    file -= 1
    return (rank * PIECE_WIDTH, file * PIECE_HEIGHT)

# piece placement
for char in sections[0]:
    if char.isalpha():
        piece = get_piece(char)
        image.paste(piece, get_offset(file, rank), mask=piece)
        piece.close()

        file += 1
    elif char.isnumeric():
        file += int(char)
    elif char == '/':
        rank += 1
        file = 1
    else:
        print(char)
        print('Error: invalid FEN')
        exit()

now = datetime.now()
image.save(now.strftime('%Y%m%d%H%M%S{}'.format('.png')))
image.close()
