from extras.Utils import *
import sys
from models import User
sys.path.append("../")
from extras.Base_Handler import BaseHandler
from API_NAME import sign_out_api
from extras.Required_Fields import check_required_valid


class SignOut(BaseHandler):

    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        pass

    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(sign_out_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        self.auth.unset_session()
        write_success_to_response(self.response, {})
