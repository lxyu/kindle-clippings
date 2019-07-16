Kindle Clippings
================

A simple python script to extract clippings from 'My Clippings.txt', organize, store and output them in a more elegant way.

Features
--------

Clippings are stored in a python dict with this structure

.. code:: py

    clips = {'book': {'position': 'clipping'}}

Msgpack was used to serialize clippings for archive.

Each new `My Clippings.txt` will add clips to previous archive automatically.

Clips will be export to `output` directory, find them there.

It's EASY and you don't need to care nothing!


Usage
-----

Install `msgpack-python` first.

.. code:: bash

    $ pip install msgpack-python

Clone project and put `My\ Clippings.txt` to project's root.

Python 2
-------

Run `kindle.py`

.. code:: bash

    $ python kindle.py

DONE!

Python 3
---------

Run `kindle_python3.py`

.. code:: bash

    $ python3 kindle_python3.py

DONE!


Demo
----

Example output files tree:

.. code:: bash

    $ tree .
    .
    ├── My Clippings.txt
    ├── README.rst
    ├── clips.msgpack
    ├── kindle.py
    ├── kindle_python3.py
    └── output
        ├── Hackers & Painters (Paul Graham).txt
        ├── Life of Pi (Yann Martel).txt

Example output file contet:

    Nerds aren't losers. They're just playing a different game, and a game much closer to the one played in the real world. Adults know this. It's hard to find successful adults now who don't claim to have been nerds in high school.

    ---

    What hackers and painters have in common is that they're both makers. Along with composers, architects, and writers, what hackers and painters are trying to do is make good things. They're not doing research per se, though if in the course of trying to make good things they discover some new technique, so much the better.

    ---

    This is not a problem for big companies, because they don't win by making great products. Big companies win by sucking less than other big companies.

