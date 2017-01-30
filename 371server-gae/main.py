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
import logging
import os

from google.appengine.ext.webapp import template

import webapp2
import json

from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from models.listing import Listing
from models.user import User


def user_required(handler):
    """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
    """
    def check_signin(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('signin'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_signin


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property"""
        return  auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session

        The list of attributes to store in the session is specified in
            config['webapp2_extras.auth']['user_attributes'].
        :returns
            A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged-in user.

        Unlike user_info, it fetches information from the persistence layer and
            returns an instance of the underlying model.
        :returns
            The instance of the user model associated to the signed-in user.
        """
        user = self.user_info
        return self.user_model.get_by_id(user['user_id']) if user else None

    @webapp2.cached_property
    def user_model(self):
        """Return the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        user = self.user_info
        params['user'] = user
        path = os.path.join(os.path.dirname(__file__), view_filename)
        self.response.out.write(template.render(path, params))

    def display_message(self, message):
        """Utility function to display a template with a simple message"""
        params = {
            'message': message
        }
        self.render_template('message.html', params)

    # this is needed for webapp2 sessions to work
    def dispatch(self):
        # get a session for webapp2 sessions to work
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions
            self.session_store.save_sessions(self.response)




class MainHandler(BaseHandler):
    def get(self):
        self.render_template('home.html')


class CreateUser(BaseHandler):
    def get(self):
        self.render_template('create_user.html')

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

        unique_properties = ['email_address']
        user_data = self.user_model.create_user(email, unique_properties, email_address=email,
              first_name=first_name, password_raw=password, phone1=phone1, phone2=phone2, phone3=phone3,
              province=province, city=city, last_name=last_name, verified=False)
        if not user_data[0]: # user_data is a tuple
            self.display_message('Unable to create user for email %s because of \
                                 duplicate keys %s' % (email, user_data[1]))
            return

        user = user_data[1]
        user_id = user.get_id()

        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='v', user_id=user_id,
                                        signup_token=token, _full=True)

        msg = 'Send an email to user in order to verify their address. \
                  They will be able to do so by visiting <a href="{url}">{url}</a>'

        self.display_message(msg.format(url=verification_url))


        # user = User(first_name=first_name, last_name=last_name, email=email, password=password,
        #             phone1=phone1, phone2=phone2, phone3=phone3, province=province, city=city)
        # key = User.build_key(email)
        # user.key = key
        # user.put()
        # self.response.out.write('<h1>Registered!</h1>')


class SignIn(BaseHandler):

    def get(self):
        # template_values = {
        #
        # }
        # # test = json.dumps(template_values)
        # path = os.path.join(os.path.dirname(__file__), 'sign_in.html')
        # self.response.out.write(template.render(path, template_values))
        self._serve_page()

    def post(self):
        user_email = self.request.get('email')
        password = self.request.get('password')
        # user = User.query(User.key == User.build_key(user_email), User.password == password).get()
        try:
            u = self.auth.get_user_by_password(user_email, password, remember=True,
                                               save_session=True)
            self.redirect(self.uri_for('home'))
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s', user_email, type(e))
            self._serve_page(True)
       # listings = Listing.query(Listing.lister_email == user_email).fetch()


    def _serve_page(self, failed=False):
        user_email = self.request.get('email')
        params = {
            'user_email': user_email,
            'failed': failed
        }
        self.render_template('sign_in.html', params)



class ForgotPasswordHandler(BaseHandler):
    def get(self):
        self._serve_page()

    def post(self):
        email = self.request.get('email')
        user = self.user_model.get_by_auth_id(email)
        if not user:
            logging.info('Could not find any user entry for email %s', email)
            self._serve_page(not_found=True)
            return
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='p', user_id=user_id,
                                        signup_token=token, _full=True)

        msg = 'Send an email to user in order to reset their password. \
                  They will be able to do so by visiting <a href="{url}">{url}</a>'

        self.display_message(msg.format(url=verification_url))

    def _serve_page(self, not_found=False):
        username = self.request.get('username')
        params = {
            'username': username,
            'not_found': not_found
        }
        self.render_template('forgot.html', params)

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
        bedrooms = int(self.request.get('bedrooms'))
        sqft = int(self.request.get('sqft'))
        bathrooms = int(self.request.get('bathrooms'))
        price = int(self.request.get('price'))
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

class ShowListings(webapp2.RequestHandler):
    def get(self):
        #TODO: Remove testing account, should pass in user email as parameter
        user = User.query(User.key == User.build_key('test@gmail.com')).get()
        listings = Listing.query(Listing.lister_email == user.email).fetch()
        path = os.path.join(os.path.dirname(__file__), 'show_listings.html')
        for listing in listings:
            template_values = {
                'lister_email': listing.lister_email,
                'bedrooms': listing.bedrooms,
                'sqft': listing.sqft,
                'bathrooms': listing.bathrooms,
                'price': listing.price,
                'description': listing.description,
                'isPublished': listing.isPublished,
                'province': listing.province,
                'city': listing.city,
                'images': listing.images #TODO: store image URLs from blobstore to a list
            }
            self.response.out.write(template.render(path, template_values))


class VerificationHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user = None
        user_id = kwargs['user_id']
        signup_token = kwargs['signup_token']
        verification_type = kwargs['type']

        user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token, 'signup')

        if not user:
            logging.info('Could not find any user with id "%s" signup token "%s"',
                         user_id, signup_token)
            self.abort(404)

        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

        if verification_type == 'v': #remove signup token, we don't want users to come back with an old link
         self.user_model.delete_signup_token(user.get_id(), signup_token)

        if not user.verified:
            user.verified = True
            user.put()

            self.display_message('User email address has been verified.')
            return
        elif verification_type == 'p':
            # supply user to the page
            params = {
                'user': user,
                'token': signup_token
            }
            self.render_template('resetpassword.html', params)
        else:
            logging.info('verification type not supported.')
            self.abort(404)


class SetPasswordHandler(BaseHandler):

    @user_required
    def post(self):
        password = self.request.get('password')
        old_token = self.request.get('t')

        if not password or password != self.request.get('confirm_password'):
            self.display_message('passwords do not match')
            return

        user = self.user
        user.set_password(password)
        user.put()

        # remove sign up token, we don't want user to come back with an old link
        self.user_model.delete_signup_token(user.get_id(), old_token)
        self.display_message('Password updated.')



class AuthenticatedHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('authenticated.html')


class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect(self.uri_for('home'))

config = {
    'webapp2_extras.auth': {
        'user_model': User,
        'user_attributes': ['first_name', 'phone1', 'phone2', 'phone3', 'province', 'city']
    },
    'webapp2_extras.sessions':{
        'secret_key': 'YOUR_SECRET_KEY'
    }
}

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/createuser', CreateUser),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
      handler=VerificationHandler, name='verification'),
    webapp2.Route('/signin', SignIn, name='signin'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    webapp2.Route('/createlisting', CreateListing),
    webapp2.Route('/showlistings', ShowListings)
], debug=True, config=config)
