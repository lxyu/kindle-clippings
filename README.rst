Kindle Clippings
================

A simple python script to extract clippings from 'My Clippings.txt', organize, store and output them in a more elegant way.

Features
--------

Clippings are stored in a python dict with this structure

.. code:: py

    clips = {'book': {'position': 'clipping'}}

Msgpack was used to serialize clippings for archive.

Each new `My\ Clippings.txt` will add clips to previous archive automatically.

Clips will be export to `output` directory, find them there.

It's EASY and you don't need to care nothing!


Usage
-----

Install `msgpack-python` first.

.. code:: bash

    $ pip install msgpack

Clone project and put `My\ Clippings.txt` to project's root.

Run `kindle.py`

.. code:: bash

    $ python kindle.py

DONE!
