from extras.utils import *

sys.path.append("../")
from extras.Base_Handler import BaseHandler


class SignOut(BaseHandler):
    def get(self):
        pass

    def post(self):
        self.auth.unset_session()