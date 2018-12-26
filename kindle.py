#!/usr/bin/env python3
# work with Python 3.3+ only
# -*- coding: utf-8 -*-

import os
import sys
import re
import json
import argparse
import dateparser
if __name__ == '__main__':
    from db_adapter import KindleClippingDB
else:
    from .db_adapter import KindleClippingDB

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

    clip['content'] = lines[2]
    
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
    

    ##TODO: There are some cases where location be recorded in different format:
     ##  - 您在第 5 页（位置 #111）的书签 | 添加于 2017年2月23日星期四 上午8:00:46
    position_match = re.search(r'(\d+)-(\d+)', lines[1])
    if position_match:
        clip['position'] = int(position_match.group(1))
        clip['position_end'] = int(position_match.group(2))
    

    #TODO: i18n support . for example , chinese version of Kindle have the below format
     ## - 您在位置 #180-180的标注 | 添加于 2017年2月22日星期三 下午7:06:30
    date_match = re.search(r'Added on (.+)$', lines[1])
    if date_match:
        date_str = date_match.group(1)
        date_time_obj = dateparser.parse(date_string = date_str)
        epoch = date_time_obj.timestamp()
        clip['date'] = int(epoch)

    #TODO: To recognise Notes & bookmark. notes have different format with highlight.
    #Note: - Your Note on page 187 | Location 2850 | Added on Wednesday, July 4, 2018 5:43:04 PM
    #Bookmark: - Your Bookmark on Location 15572 | Added on Tuesday, July 24, 2018 10:42:15 AM
    
    return clip



def main(kindle_clippings_file_path, json_db_path , is_overwrite):
    db = KindleClippingDB(json_db_path)

    if is_overwrite:
        db.pure_all()

    #import ipdb; ipdb.set_trace()        
    sections = get_sections(kindle_clippings_file_path)
    with db.db:
        for section in sections:
            clip = get_clip(section)
            try:
                if clip:
                    db.add_highlight(clip['content'],clip['title'],clip['author'],clip['position'],clip['position_end'],clip['date'])
            except KeyError:
                print("missing minimum attribute {}".format(str(clip)))


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
