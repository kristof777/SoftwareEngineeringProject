import sys
from extras.utils import *
from models.Listing import Listing
from models.Message import Message
from models.User import User
sys.path.append("../")


class GetMessages(webapp2.RequestHandler):
    """
     Class used to handle get and post.
     Get:  do nothing
     Post:
         @pre-cond: Expecting keys to be userId
         @post-cond: all the messages that sent to me
     """

    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = ['userId', 'authToken']

        errors, values = keys_missing(error_keys, self.request.POST)
        if len(errors) != 0:
            write_error_to_response(self.response, errors,
                                    missing_invalid_parameter)
            return

        # check validity for integer fields (userId)
        invalid = key_validation(values)

        if len(invalid) != 0:
            write_error_to_response(self.response, invalid,
                                    missing_invalid_parameter)
            return

        # find the correct user with userId
        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'User not authorized'
            }
            write_error_to_response(self.response, error, not_authorized)
            return

        # Check if it is the valid user
        valid_user = user.validate_token(int(values["userId"]),
                                         "auth",
                                         values["authToken"])
        if not valid_user:
            write_error_to_response(self.response, {not_authorized['error']:
                                                        "not authorized to get my messages"},
                                    not_authorized['status'])
            return

        user_id = int(values['userId'])
        my_messages = Message.query(Message.receiverId == user_id).fetch()
        returned_array = []
        for my_message in my_messages:
            template_values = {
                'messageId': my_message.messageId,
                'listingId': my_message.listingId,
                'senderId': my_message.senderId,
                'message': my_message.message,
                'phone': my_message.phone,
                'email': my_message.email,
                'received': my_message.received,
                'createdDate': str(my_message.createdDate)
            }
            returned_array.append(template_values)

        write_success_to_response(self.response, {"messages": returned_array})































