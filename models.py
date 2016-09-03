from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    vnos = ndb.StringProperty()
    status = ndb.BooleanProperty(default=False)
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
