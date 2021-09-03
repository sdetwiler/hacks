#!/usr/bin/env python3

import sys
import os
from PIL import Image, ImageDraw, ImageFont



def main():
    # Iterate over all images in directory and resize.

    count = 0
    directory = '.'
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg"):
            filenames.append(filename)
    for filename in sorted(filenames):
        i = Image.open(filename)
        i.resize((800, 600))
        out_filename = '{}.jpg'.format(count)
        i.save(out_filename, 'JPEG')
        count+=1

if __name__ == '__main__':
    main()
