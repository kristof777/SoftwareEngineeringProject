import webapp2
from webapp2_extras import auth
from webapp2_extras import sessions
import os
from google.appengine.ext.webapp import template
# Before writing the actual handlers that will implement the business
# logic sign up and authentication users, we will group some utility
# functions in a base handler class, which will be extended by all the
# following handler classes.
#
# This will ensure that all handlers will inherit a set of useful utility
# functions and properties to access user data and infrastructure classes,
# but also ensures that all session data is properly saved on each request.
class BaseHandler(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

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
        return self.user_model.get_by_id(user['userId']) if user else None

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
        self.render_template('../webpages/Message.html', params)

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



# home page ( for browser testing only )
class MainHandler(BaseHandler):
    def get(self):
        self.render_template('../webpages/Home.html')


# create_user is more of type POST, because we want to send all the
# info about this new user and create a new record in the database.
# The GET method here is pretty much just get the html page to show
# the login screen ( in the browser).
