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

from datetime import datetime

settings = {'debug' : True,
            'template_path':os.path.join(os.path.dirname(__file__), "templates"),
            'static_path':os.path.join(os.path.dirname(__file__), "static")
            }

limited_ip='none'
db_host='192.168.2.102'
class MainHandler(tornado.web.RequestHandler):
    def get(self):
	print self.request.remote_ip
	global limited_ip
	if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
	    return

        self.render("login.html", title="MyTitle", body='', oid=0)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        pass
    def post(self):
        pass

class QueryInfoHandler(tornado.web.RequestHandler):
    def post(self):
	global limited_ip
	if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
	    return

	global db_host
        oid = int(self.get_argument('oid'))
        client = MongoClient(db_host, 18188)
        db = client.flower
        doc = db.info.find_one({u"oid":oid}, {u"_id":0})

        if doc == None:
            oid = 0

        jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
        htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))

        self.render("infodiv.html", body=htmlcode, oid=oid)
        
class ChangeGoldHandler(tornado.web.RequestHandler):
    def post(self):
	global limited_ip
	if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
	    return

        oid = int(self.get_argument('oid'))
        newgold = long(self.get_argument('gold'))

        print oid
        print newgold

        make_inc(self, oid, "gold", newgold)
 
def make_inc(handler, oid, key, value):
    global limited_ip 
    if (handler.request.remote_ip != limited_ip and limited_ip != 'none'):
		return

    if key == 'oid' or key == 'id' or key == 'idtype':
        handler.render("infodiv.html", body="key不能是oid, id, idtype", oid=oid)
        return
    global db_host    
    client = MongoClient(db_host, 18188)
    db = client.flower
    ##key = unicode(key, "utf-8")
    ## 保存gm操作
    doclast = db.info.find_one({u"oid":oid}, {u"_id":0})
    doclast[u'gmop'] = {u'key': key, u'value':value, u'time':datetime.now(), u'op':u'inc'}
    db.gmop.insert(doclast)
    
    db.info.update({u"oid": oid}, {u"$inc":{key : value}})
    
    doc = db.info.find_one({u"oid":oid}, {u"_id":0})
    
    if doc == None:
        oid = 0
        
    jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
    htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))
    
    handler.render("infodiv.html", body=htmlcode, oid=oid)

def reset_fucker(handler, oid, key, value):
    global limited_ip 
    if (handler.request.remote_ip != limited_ip and limited_ip != 'none'):
		return

    if key == 'oid' or key == 'id' or key == 'idtype':
        handler.render("infodiv.html", body="key不能是oid, id, idtype", oid=oid)
        return
    global db_host    
    client = MongoClient(db_host, 18188)
    db = client.flower
    ##key = unicode(key, "utf-8")
    ## 保存gm操作
    doclast = db.info.find_one({u"oid":oid}, {u"_id":0})
    doclast[u'gmop'] = {u'key': key, u'value':value, u'time':datetime.now(), u'op':u'reset'}
    db.gmop.insert(doclast)
    
    db.info.update({u"oid": oid}, {u"$set":{'locked':False, 'gold': 20000, 'medal':20, 'gift.car':0, 'gift.diamond':0, 'gift.houseboat':0}})
    
    doc = db.info.find_one({u"oid":oid}, {u"_id":0})
    
    if doc == None:
        oid = 0
        
    jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
    htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))
    
    handler.render("infodiv.html", body=htmlcode, oid=oid)

def del_fucker(handler, oid, key, value):
    global limited_ip 
    if (handler.request.remote_ip != limited_ip and limited_ip != 'none'):
		return

    if key == 'oid' or key == 'id' or key == 'idtype':
        handler.render("infodiv.html", body="key不能是oid, id, idtype", oid=oid)
        return
    global db_host    
    client = MongoClient(db_host, 18188)
    db = client.flower
    ##key = unicode(key, "utf-8")
    ## 保存gm操作
    doclast = db.info.find_one({u"oid":oid}, {u"_id":0})
    doclast[u'gmop'] = {u'key': key, u'value':value, u'time':datetime.now(), u'op':u'del'}
    db.gmop.insert(doclast)
    
    db.info.update({u"oid": oid}, {u"$set":{'idtype':'deleted'}})
    
    doc = db.info.find_one({u"oid":oid}, {u"_id":0})
    
    if doc == None:
        oid = 0
        
    jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
    htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))
    
    handler.render("infodiv.html", body=htmlcode, oid=oid)


def add_item(handler, oid, key, value):
	global limited_ip


	print "dsfsfdsfdsf1"
	if (handler.request.remote_ip != limited_ip and limited_ip != 'none'):
		print "dsfsfdsfdsf1213"
		return
	if key == 'oid' or key == 'id' or key == 'idtype':
		print "dsfsfdsfdsf121323"
		handler.render("infodiv.html", body="key不能是oid, id, idtype", oid=oid)
		return

	print "dsfsfdsfdsf2"
	global db_host    
	client = MongoClient(db_host, 18188)
	db = client.flower
    ##key = unicode(key, "utf-8")
    ## 保存gm操作
	doclast = db.info.find_one({u"oid":oid}, {u"_id":0})
	doclast[u'gmop'] = {u'key': key, u'value':value, u'time':datetime.now(), u'op':u'addItem'}
	db.gmop.insert(doclast)

	new_key = u"bag."+key+u".id"

	print new_key
	
	db.info.update({u"oid": oid}, {u"$set":{u"bag."+key+u".id" : int(key)}, u"$inc":{u"bag."+key+u".count" : int(value)}})
	
	doc = db.info.find_one({u"oid":oid}, {u"_id":0})

	print "dsfsfdsfdsf"
	 
	if doc == None:
	    oid = 0
	    
	jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
	htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))
	
	handler.render("infodiv.html", body=htmlcode, oid=oid)
      
def make_change(handler, oid, key, value):
    global limited_ip 
    if (handler.request.remote_ip != limited_ip  and limited_ip != 'none'):
		return

    if key == 'oid' or key == 'id' or key == 'idtype':
        handler.render("infodiv.html", body="key不能是oid, id, idtype", oid=oid)
        return
    global db_host    
    client = MongoClient(db_host, 18188)
    db = client.flower
    ##key = unicode(key, "utf-8")
    ## 保存gm操作
    doclast = db.info.find_one({u"oid":oid}, {u"_id":0})
    doclast[u'gmop'] = {u'key': key, u'value':value, u'time':datetime.now()}
    db.gmop.insert(doclast)
    
    db.info.update({u"oid": oid}, {u"$set":{key : value}})
    
    doc = db.info.find_one({u"oid":oid}, {u"_id":0})
    
    if doc == None:
        oid = 0
        
    jsoncode = json.dumps(doc, sort_keys=True, indent=4, ensure_ascii=False)
    htmlcode = highlight(jsoncode, JsonLexer(encoding='utf-8'), HtmlFormatter(encoding='utf-8', cssclass="highlight"))
    
    handler.render("infodiv.html", body=htmlcode, oid=oid)

    
class ChangeAnyHandler(tornado.web.RequestHandler):
    def post(self):
	global limited_ip
	if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
	    return
        oid = int(self.get_argument('oid'))
        key = self.get_argument('key')
        value = int(self.get_argument('value'))

        print oid
        print key
        print value

        make_change(self, oid, key, value)
        
class ChangeAnyBooleanHandler(tornado.web.RequestHandler):
   def post(self):
       global limited_ip
       if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
           return
       oid = int(self.get_argument('oid'))
       key = self.get_argument('key')
       value = self.get_argument('value') == "true" and True or False

       print oid
       print key
       print value

       make_change(self, oid, key, value)
       
class ChangeAnyStringHandler(tornado.web.RequestHandler):
   def post(self):
       global limited_ip
       if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
           return

       oid = int(self.get_argument('oid'))
       key = self.get_argument('key')
       value = self.get_argument('value')

       print oid
       print key
       print value

       make_change(self, oid, key, value)
 
class AddItemHandler(tornado.web.RequestHandler):
   def post(self):
       global limited_ip
       if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
           return

       oid = int(self.get_argument('oid'))
       key = self.get_argument('key')
       value = self.get_argument('value')

       print oid
       print key
       print value

       add_item(self, oid, key, value)

class ResetFuckerHandler(tornado.web.RequestHandler):
    def post(self):
       global limited_ip
       if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
           return

       oid = int(self.get_argument('oid'))
       key = self.get_argument('key')
       value = self.get_argument('value')

       print oid
       print key
       print value

       reset_fucker(self, oid, key, value)

class DelFuckerHandler(tornado.web.RequestHandler):
    def post(self):
       global limited_ip
       if (self.request.remote_ip != limited_ip and limited_ip != 'none'):
           return

       oid = int(self.get_argument('oid'))
       key = self.get_argument('key')
       value = self.get_argument('value')

       print oid
       print key
       print value

       del_fucker(self, oid, key, value)


      
application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/change_gold", ChangeGoldHandler),
        (r"/query_info", QueryInfoHandler),
        (r"/change_any", ChangeAnyHandler),
        (r"/change_any_boolean", ChangeAnyBooleanHandler),
        (r"/change_any_string", ChangeAnyStringHandler),
		(r"/add_item", AddItemHandler),
		(r"/reset_fucker", ResetFuckerHandler),
		(r"/del_fucker", DelFuckerHandler)
        ], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
