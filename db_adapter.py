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
    
    def _add_highlight(self,book_id,content,epoch,pos_start,pos_end,other_attrs):
        hQ = Query()
        res = self.highlights.search((hQ.book_id == book_id) & (hQ.content == content))
        if len(res) > 0:
            return res[0].doc_id 
        doc = dict(other_attrs)
        doc['book_id'] = book_id
        doc['content'] = content
        doc['pos_start'] = pos_start if pos_start else 0 
        doc['pos_end'] = pos_end if pos_end else 0
        doc['epoch'] = epoch if epoch else 0
        id =  self.highlights.insert(doc)
        return id

    def add_highlight(self,content,book_title,book_author,epoch,pos_start = None,pos_end = None,other_attrs = {}):
        res = self.query_book(book_title,book_author)
        book_id = None
        if len(res)>0 :
            book_id = res[0].doc_id
        else:
            book_id = self.add_book(book_title,book_author)
        id = self._add_highlight(book_id,content,epoch,pos_start,pos_end,other_attrs)
        return id

    def query_book(self,title,author):
        bookQ = Query()
        def author_name_matcher(db_value,input_value):
            db_names = set([x for x in re.split(r'\s|,', db_value) if len(x)>0])
            input_names = set([x for x in re.split(r'\s|,', input_value) if len(x)>0])
            return db_names == input_names

        def author_name_matcher_fallback(db_value,input_value):
            db_value = db_value.lower()
            input_value = input_value.lower()
            if ( db_value.find(input_value) != -1 or input_value.find(db_value) != -1):
                return True
            else:
                return False 
        res = self.books.search((bookQ.title == title) & (bookQ.author.test(author_name_matcher,author)))
        if (len(res) < 1):
            res = self.books.search((bookQ.title == title) & (bookQ.author.test(author_name_matcher_fallback,author)))
        return res

    def get_highligts_by_book(self,book_title,book_author,book_query = None):
        books = self.query_book(book_title,book_author)
        if not books :
            return []
        res = []
        for b in books:
            if book_query:
                q = (((Query().book_id == b.doc_id) & book_query) & ( ~ Query().hidden_mark.exists() ))
            else:
                q = ((Query().book_id == b.doc_id)  &  ( ~ Query().hidden_mark.exists() ) )
            res.extend(self.highlights.search(q))
        return res
    