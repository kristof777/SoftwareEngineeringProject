from __future__ import absolute_import

import os
import sys
sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.utils import *
from models.User import User
import Main
from models.FB import FBLogin

class TestFacebookLogin(unittest.TestCase):
    """

    """

    def setUp(self):
        setup_testbed(self)
        self.users = create_dummy_users_for_testing(Main, 3)
        input = create_random_user()
        input["fbId"] = "1212312398"
        response_body, status_int = get_response_from_post(Main, input,
                                                           "createUser")
        self.assertEquals(status_int, success)
        self.assertTrue("authToken" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))
        self.assertEquals(user_saved.first_name,input["firstName"])
        self.assertEquals(user_saved.last_name,input["lastName"])
        self.assertEquals(user_saved.city,input["city"])
        self.assertEquals(user_saved.email,input["email"])
        self.assertEquals(user_saved.phone1,input["phone1"])
        self.assertEquals(user_saved.province,input["province"])
        fb_e_id = FBLogin.query().fetch(keys_only=True)[0].integer_id()
        fb_e = FBLogin.get_by_id(fb_e_id)
        self.assertEquals(fb_e.user_id,int(response_body["userId"]))
        self.assertEquals(fb_e.fb_id, int(input["fbId"]))




    def test_success_facebook_login(self):
        get_response_from_post(Main, {"fbId":1212312398}, "fbLogin")










def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()