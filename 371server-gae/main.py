#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#############################################################################################
# Download google app engine: https://cloud.google.com/appengine/docs/python/download
# choose the option "Or, you can download the original App Engine SDK for Python."
# local host: 127.0.0.1:8080
#############################################################################################

import os

from google.appengine.ext.webapp import template

import webapp2
import json

from models.listing import Listing
from models.user import User


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('<h1>hello!</h1>')


class CreateUser(webapp2.RequestHandler):
    def get(self):
        template_values = {
            # 'first_name': user2.first_name,
            # 'last_name': user2.last_name
        }
        path = os.path.join(os.path.dirname(__file__), 'create_user.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        first_name = self.request.get('firstName')
        last_name = self.request.get('lastName')
        email = self.request.get('email')
        password = self.request.get('password')
        phone1 = self.request.get('phone1')
        phone2 = self.request.get('phone2')
        phone3 = self.request.get('phone3')
        province = self.request.get('province')
        city = self.request.get('city')

        user = User(first_name=first_name, last_name=last_name, email=email, password=password,
                    phone1=phone1, phone2=phone2, phone3=phone3, province=province, city=city)
        key = User.build_key(email)
        user.key = key
        user.put()
        self.response.out.write('<h1>Registered!</h1>')


class SignIn(webapp2.RequestHandler):

    def get(self):
        template_values = {

        }
        # test = json.dumps(template_values)
        path = os.path.join(os.path.dirname(__file__), 'sign_in.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        user_email = self.request.get('email')
        password = self.request.get('password')
        user = User.query(User.key == User.build_key(user_email), User.password == password).get()
        listings = []
        listings = Listing.query(Listing.lister_email == user_email).get()
        # should return user info and listings back
        self.response.out.write('<h1>Signed in!</h1>')


class CreateListing(webapp2.RequestHandler):
    def get(self):
        #TODO: Should pass in user email as parameter
        template_values = {
            # 'first_name': user2.first_name,
            # 'last_name': user2.last_name
        }
        # test = json.dumps(template_values)
        path = os.path.join(os.path.dirname(__file__), 'create_listing.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

       #TODO: Remove testing account
        user = User.query(User.key == User.build_key('test@gmail.com')).get()
        lister_email = user.email
        bedrooms = self.request.get('bedrooms')
        sqft = self.request.get('sqft')
        bathrooms = self.request.get('bathrooms')
        price = self.request.get('price')
        description = self.request.get('description')
        isPublished = self.request.get('isPublished') != ''
        province = user.province
        city = user.city
        images = self.request.get('images')

        listing = Listing(lister_email=lister_email, bedrooms=bedrooms, sqft=sqft, bathrooms=bathrooms,
                          price=price, description=description, isPublished=isPublished, province=province,
                          city=city, images=images)
        key = Listing.build_key(lister_email, bedrooms, sqft, bathrooms, price, description, province, city)
        listing.key = key
        listing.put()

        self.response.out.write('<h1>New listing created!</h1>')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/createuser', CreateUser),
    ('/signin', SignIn),
    ('/createlisting', CreateListing)
], debug=True)
