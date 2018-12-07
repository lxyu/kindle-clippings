#!/usr/bin/env python3
# work with Python 3.3+ only
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import argparse
import collections
from io import open

BOUNDARY = u"=========="

def get_sections(path):
    with open(path, 'r',encoding='utf8') as f:
        content = f.read()
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)


def get_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]
    match = re.search(r'(\d+)-\d+', lines[1])
    if not match:
        return
    position = match.group(1)

    clip['position'] = int(position)
    clip['content'] = lines[2]

    return clip


def load_clips(path):
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(path, 'r',encoding='utf8') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}

def save_clips(clips , output_path):
    """
    Save new clips to DATA_FILE
    """
    with open(output_path, 'w',encoding='utf8' ) as f:
        json_string = json.dumps(clips, ensure_ascii=False ,indent=2)
        f.write(json_string)


def main(kindle_clippings_file_path, output_path , is_overwrite):
    clips = collections.defaultdict(dict)
    
    if not is_overwrite and os.path.isfile(output_path):
        # load old clips        
        clips.update(load_clips(output_path))

    #import ipdb; ipdb.set_trace()        

    # extract clips
    sections = get_sections(kindle_clippings_file_path)
    for section in sections:
        clip = get_clip(section)
        if clip:
            clips[clip['book']][str(clip['position'])] = clip['content']

    # remove key with empty value
    clips = {k: v for k, v in clips.items() if v}

    # save/export clips
    save_clips(clips,output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kindle clipping to JSON parser')
    parser.add_argument('clippings_file',type=str ,help="Kindle My Clippings.txt file path")
    parser.add_argument('--overwrite' , nargs='?', const='True', help="By defult your new JSON file will based on previous parsed JSON,if you have assigned this argument new content will overwrite old one.")
    parser.add_argument('--output',default="./clips.json", type=str , help="parsed JSON file path")
    args = parser.parse_args()
    if not os.path.isfile(args.clippings_file):
        print("You need to feed me a 'My Clippings.txt' file")
        sys.exit(-1)

    is_overwrite = False
    if args.overwrite.lower() == "true":
        is_overwrite = True

    main(args.clippings_file , args.output , is_overwrite)
