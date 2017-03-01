from extras.utils import *
sys.path.append("../")
from extras.Base_Handler import BaseHandler


class ContactSeller(BaseHandler):
    def get(self):
        pass

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = ['userId', 'listingId', 'message','phone1',
                      'email', 'phone2']
        errors, values = keys_missing(error_keys, self.request.POST)
        print(errors)





