from __future__ import absolute_import
import sys
from extras.Error_Code import *
from extras.Required_Fields import required_api_dict

sys.path.append('../')
import os
import unittest
import Main
from API_NAME import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Utils import *
from extras.Check_Invalid import *
from extras.Random_Models import *


class TestUtils(unittest.TestCase):


    def setUp(self):
        setup_testbed(self)


    def test_keys_missing(self):
        keys = required_api_dict[sign_in_token_api]
        errors, values = keys_missing(keys,{})
        self.assertEquals(errors, {'missingToken': 'authToken is Missing',
                                   'missingUserId': 'userId is Missing'})


    def tearDown(self):
        self.testbed.deactivate()
