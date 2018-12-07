#!/usr/bin/env python3
# work with Python 3.3+ only
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import argparse
import dateparser
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
    positon_match = re.search(r'(\d+)-\d+', lines[1])
    if not positon_match:
        return
    position = positon_match.group(1)

    date_match = re.search(r'Added on (.+)$', lines[1])
    if not date_match:
        return
    date_str = date_match.group(1)
    
    date_time_obj = dateparser.parse(date_string = date_str)
    epoch = date_time_obj.timestamp()
    
    clip['position'] = int(position)

    clip['date'] = int(epoch)

    title_author_content = lines[0]    
    reversed_str = ''.join(list(reversed([c for c in title_author_content])))
    res  = re.search(r'\)(.+?)\((.+)$',reversed_str)
    if res:
        author = ''.join(list(reversed([c for c in res.group(1)])))
        author = re.sub(r'\(|\)',' ',author)
        
        title = ''.join(list(reversed([c for c in res.group(2)])))
        title = title.strip('(').strip(')')
    else:
        title = title_author_content
        author = ''

    clip['title'] = title
    clip['author'] = author

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
            clips[clip['book']][str(clip['position'])] = {'content': clip['content'],
                                                          'author':clip['author'],
                                                          'title':clip['title'],
                                                          'date':clip['date']
                                                          }

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
    if args.overwrite and args.overwrite.lower() == "true":
        is_overwrite = True

    main(args.clippings_file , args.output , is_overwrite)
