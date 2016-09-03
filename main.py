#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from models import Sporocilo


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        seznam1 = Sporocilo.query(Sporocilo.status == False).fetch()
        seznam = Sporocilo.query(Sporocilo.status == True).fetch()
        params = {"seznam": seznam, "seznam1": seznam1}
        return self.render_template("base.html", params=params)

    def post(self):
        vnos = self.request.get("vnos")
        sporocilo = Sporocilo(vnos=vnos)
        sporocilo.put()
        return self.redirect_to("seznam-taskov")


class PosamezenTaskHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("posamezen_task.html", params=params)


class UrediTaskHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("uredi_task.html", params=params)

    def post(self, sporocilo_id):
        vnos = self.request.get("vnos")
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.vnos = vnos
        sporocilo.put()
        return self.redirect_to("seznam-taskov")


class IzbrisiTaskHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("izbrisi_task.html", params=params)

    def post(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        sporocilo.key.delete()
        return self.redirect_to("seznam-taskov")


class StatusTaskHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        return self.render_template("status_task.html", params=params)

    def post(self, sporocilo_id):
        vnos = self.request.get("vnos")
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        if vnos == "1":
            sporocilo.status = True
            sporocilo.put()
            return self.redirect_to("seznam-taskov")
        if vnos == "2":
            sporocilo.status = False
            sporocilo.put()
            return self.redirect_to("seznam-taskov")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/task/<sporocilo_id:\d+>', PosamezenTaskHandler),
    webapp2.Route('/task/<sporocilo_id:\d+>/uredi', UrediTaskHandler),
    webapp2.Route('/task/<sporocilo_id:\d+>/izbrisi', IzbrisiTaskHandler),
    webapp2.Route('/task/<sporocilo_id:\d+>/status', StatusTaskHandler),
    webapp2.Route('/', MainHandler, name="seznam-taskov"),
], debug=True)
