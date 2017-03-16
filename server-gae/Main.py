#!/usr/bin/env python
# coding=utf-8
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
# local host: http://127.0.0.1:8912
# admin server page: http://localhost:9000
#############################################################################################

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
# use_library('django', '0.96')
# webapp_django_version = '0.96'
from web_apis.Sign_In import SignIn
from web_apis.Create_User import *
from web_apis.Create_Listing import *
from web_apis.Get_My_Listings import *
from web_apis.Like_Dislike_Listing import *
from web_apis.Edit_Listing import *
from web_apis.Get_Favourites import *
from web_apis.Change_Password import *
from web_apis.Sign_In_With_Token import *
from models.User import User
from extras.User_Auth import *
from web_apis.Edit_User import EditUser
from web_apis.Get_Listings import GetListing
from web_apis.Confirm_Email import VerificationHandler
from web_apis.Delete_Listing import *
from web_apis.Contact_Seller import ContactSeller
from web_apis.Edit_Message import EditMessage
from web_apis.FB_Login import FacebookLogin
from web_apis.Get_Messages import GetMessages
from web_apis.Initialize_DB_Testers import InitializeDB

# configuration
config = {
    'webapp2_extras.auth': {
        'user_model': User,
        'user_attributes': ['email', 'first_name', 'last_name', 'phone1', 'phone2', 'province', 'city']
    },
    'webapp2_extras.sessions':{
        'secret_key': 'YOUR_SECRET_KEY'
    }
}


# All API endpoints we are currently using
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/createUser', CreateUser),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
    handler=VerificationHandler, name='verification'),
    webapp2.Route('/signIn', SignIn, name='signIn'),
    webapp2.Route('/signInWithToken', SignInWithToken, name='signInWithToken'),
    webapp2.Route('/signOut', LogoutHandler, name='signOut'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/changePassword', ChangePassword),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    webapp2.Route('/createListing', CreateListing),
    webapp2.Route('/like', LikeDislikeListing),
    webapp2.Route('/editListing', EditListing),
    webapp2.Route('/getFavourites', GetFavourites),
    webapp2.Route('/getMyListings', GetMyListing),
    webapp2.Route('/editUser', EditUser),
    webapp2.Route('/getListings', GetListing),
    webapp2.Route('/deleteListing', DeleteListing),
    webapp2.Route('/contactSeller', ContactSeller),
    webapp2.Route('/editMessage', EditMessage),
    webapp2.Route('/fbLogin', FacebookLogin),
    webapp2.Route('/getMessages', GetMessages),
    webapp2.Route('/initDBTESTERS', InitializeDB)





    # webapp2.Route('/showlistings', ShowListings)
], debug=True, config=config)
