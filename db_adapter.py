# -*- coding: utf-8 -*-

from tinydb import TinyDB , Query

class KindleClippingDB(object):

    def __init__(self, db_path):
        self.db = TinyDB(db_path)
        self.books = db.table('books')
        self.highlights = db.table('highlights')

    def pure_all(self):
        self.purge_tables()

    def add_book(self, title , author )
