#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msgpack
import collections

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.msgpack"


def get_sections(filename):
    with open(filename, 'r') as f:
        content = f.read().decode('utf-8')
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)


def get_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]
    clip['position'] = lines[1][26:lines[1].rfind('-')]
    clip['content'] = lines[2]

    return clip


def export_txt(clips):
    """
    Export each book's clips to single text.
    """
    for book in clips:
        lines = []
        with open(u"%s.txt" % book, 'w') as f:
            for pos in sorted(clips[book]):
                lines.append(clips[book][pos].encode('utf-8'))

            f.write("\n--\n".join(lines))


def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'r') as f:
            return msgpack.unpack(f)
    except IOError:
        return {}


def save_clips(clips):
    """
    Save new clips to DATA_FILE
    """
    with open(DATA_FILE, 'wb') as f:
        f.write(msgpack.packb(clips))


def main():
    # load old clips
    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    # extract clips
    sections = get_sections(u'My Clippings.txt')
    for section in sections:
        clip = get_clip(section)
        if clip:
            clips[clip['book']][clip['position']] = clip['content']

    # save/export clips
    save_clips(clips)
    export_txt(clips)


if __name__ == '__main__':
    main()
