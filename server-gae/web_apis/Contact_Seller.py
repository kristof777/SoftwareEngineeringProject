from extras.utils import *
from models.Listing import Listing
from models.User import User
import sys

from models.Message import Message

sys.path.append("../")
from extras.Base_Handler import BaseHandler


class ContactSeller(BaseHandler):
    def get(self):
        pass

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = ['senderId', 'listingId', 'message', 'phone',
                      'email', 'authToken', 'receiverId']
        errors, values = keys_missing(error_keys, self.request.POST)
        if len(errors) != 0:
            write_error_to_response(self.response, errors, missing_invalid_parameter)
            return

        invalid = key_validation(values)
        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter)

        # find the correct sender with senderId
        sender = User.get_by_id(int(values['senderId']))
        if sender is None:
            error = {
                not_authorized['error']: 'Sender not authorized'
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        # check if the sender is a valid user
        valid_sender = sender.validate_token(int(values['senderId']), "auth", values['authToken'])
        if not valid_sender:
            write_error_to_response(self.response, {not_authorized['error']:
                                                    "not authorized to send messages"},
                                    not_authorized['status'])
            return

        # find the correct listing with listingId
        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: "listingId not authorized"
            }
            write_error_to_response(self.response, error, un_auth_listing['status'])
            return

        # make sure the sender is not the owner of the listing
        if int(values['senderId']) == listing.userId:
            error = {
                unallowed_message_send['error']: "Can't send message to yourself"
            }
            write_error_to_response(self.response, error, unallowed_message_send['status'])
            return

        # all set
        message = Message(senderId=int(values['senderId']),
                          listingId=int(values['listingId']),
                          message=values['message'],
                          phone=values['phone'],
                          email=values['email'],
                          receiverId = int(listing.userId)
                          )
        message.put()
        message.messageId = message.key.id()
        message.put()
        write_success_to_response(self.response, {})
