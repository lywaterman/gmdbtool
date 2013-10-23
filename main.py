#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

print sys.getdefaultencoding()

import os
import tornado.ioloop
import tornado.web

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

import pymongo

from pymongo import MongoClient

import json

settings = {'debug' : True,
            'template_path':os.path.join(os.path.dirname(__file__), "templates"),
            'static_path':os.path.join(os.path.dirname(__file__), "static")
            }

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html", title="MyTitle", body='', oid=0)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass

class QueryInfoHandler(tornado.web.RequestHandler):
    def post(self):
        oid = int(self.get_argument('oid'))
        client = MongoClient('localhost', 18188)
        db = client.flower
        doc = db.info.find_one({u"oid":oid}, {u"_id":0})

        if doc == None:
            oid = 0

        jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
        htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))

        self.render("infodiv.html", body=htmlcode, oid=oid)
        
class ChangeGoldHandler(tornado.web.RequestHandler):
    def post(self):
        oid = int(self.get_argument('oid'))
        newgold = long(self.get_argument('gold'))

        print oid
        print newgold

        client = MongoClient('localhost', 18188)
        db = client.flower
        db.info.update({u"oid": oid}, {u"$set":{u"gold": newgold}})

        doc = db.info.find_one({u"oid":oid}, {u"_id":0})

        if doc == None:
            oid = 0

        jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
        htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))

        self.render("infodiv.html", body=htmlcode, oid=oid)
        

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/change_gold", ChangeGoldHandler),
        (r"/query_info", QueryInfoHandler),
        ], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
