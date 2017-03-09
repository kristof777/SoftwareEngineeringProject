from __future__ import absolute_import
import json
import os
import sys
sys.path.append("../")
import unittest
from extras.Error_Code import *
import Main
import webapp2
from models.User import User
from extras.utils import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'




class TestConfirmEmail(unittest.TestCase):
    """
    These are test, being tested
    Different kinds of empty strings and null values
    Test invalid phone 1
    Test invalid phone 2
    Test password mismatch
    Test not strong password
    Test all valid fields
    """
    def setUp(self):
        setup_testbed(self)
        self.api = "createUser"

    def test_create_user_with_email_confirmation(self):
        input = create_random_user()
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, success)
        self.assertTrue("token" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))

        messages = self.mail_stub.get_sent_messages(to=user_saved.email)
        self.assertEqual(1, len(messages))
        self.assertEqual(user_saved.email, messages[0].to)

    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




# suite = unittest.TestLoader().loadTestsFromTestCase(TestHandlers)
# unittest.TextTestRunner(verbosity=3).run(suite)
