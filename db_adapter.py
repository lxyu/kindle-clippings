# -*- coding: utf-8 -*-
import re
from tinydb import TinyDB , Query

class KindleClippingDB(object):

    def __init__(self, db_path):
        self.db = TinyDB(db_path,sort_keys=True, indent=4, ensure_ascii=False,allow_nan=False)
        self.books = self.db.table('books')
        self.highlights = self.db.table('highlights')

    def pure_all(self):
        self.db.purge_tables()

    def add_book(self, title , author ,other_attrs = {}):
        doc = dict(other_attrs)
        doc['title'] = title
        doc['author'] = author if author else ""
        id = self.books.insert(doc)
        return id
    
    def _add_highlight(self,book_id,content,pos_start,pos_end,datetime_epoch,other_attrs):
        hQ = Query()
        res = self.highlights.search((hQ.book_id == book_id) & (hQ.content == content))
        if len(res) > 0:
            return res[0].doc_id 
        doc = dict(other_attrs)
        doc['book_id'] = book_id
        doc['content'] = content
        doc['pos_start'] = pos_start
        doc['pos_end'] = pos_end if pos_end else 0
        doc['datetime_epoch'] = datetime_epoch if datetime_epoch else 0
        id =  self.highlights.insert(doc)
        return id

    def add_highlight(self,content,book_title,book_author,pos_start,pos_end,datetime_epoch,other_attrs = {}):
        res = self.query_book(book_title,book_author)
        book_id = None
        if len(res)>0 :
            book_id = res[0].doc_id
        else:
            book_id = self.add_book(book_title,book_author)
        id = self._add_highlight(book_id,content,pos_start,pos_end,datetime_epoch,other_attrs)
        return id

    def query_book(self,title,author):
        bookQ = Query()
        def author_name_matcher(db_value,input_value):
            db_names = set([x for x in re.split(r'\s|,', db_value) if len(x)>0])
            input_names = set([x for x in re.split(r'\s|,', input_value) if len(x)>0])
            return db_names == input_names
        res = self.books.search((bookQ.title == title) & (bookQ.author.test(author_name_matcher,author)))
        return res

    def get_highligts_by_book(self,book_title,book_author):
        books = self.query_book(book_title,book_author)
        if not books :
            return []
        res = []
        for b in books:
            res.extend(self.highlights.search(Query().book_id == b.doc_id))
        return res
    