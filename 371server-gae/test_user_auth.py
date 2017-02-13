import unittest
import webapp2

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import main
from httplib import BadStatusLine
import json





class TestHandlers(unittest.TestCase):
    def test_createuser(self):

        request = webapp2.Request.blank('/createuser') # api you need to test
        request.method = 'POST' # type of method you need to test
        something = {'username' : 'abc'} # Json object you need to send
        request.body = json.dumps(something) # actually sending it
        response = request.get_response(main.app) # get response back
        self.assertEquals(response.status_int, 400) # unit testing example checking if status is what we expected
        erros_expected = [ "api.error.missing_province" ,
                           "api.error.missing_confirmed_password",
                           "api.error.missing_password",
                           "api.error.missing_lastname",
                           "api.error.missing_phone1",
                           "api.error.missing_firstname",
                           "api.error.missing_postalcode",
                           "api.error.missing_city" ]

        error_keys = [ str(x) for x in json.loads(response.body) ]
        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(erros_expected).difference(set(error_keys))), 0)



if __name__ == '__main__':
    unittest.main()
