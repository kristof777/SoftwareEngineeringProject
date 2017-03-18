import sys

from extras.utils import *
from models.Message import Message
from models.User import User

sys.path.append("../")


class EditMessage(webapp2.RequestHandler):
    """
     Class used to handle get and post.
     Get:  do nothing
     Post:
         @pre-cond: Expecting keys to be messageId, readDel
         @post-cond: Message is either deleted for modified
         @return-api: Nothing is being returned in this API
     """

    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        self.response.out.write()

    def post(self):
        setup_post(self.response)
        error_keys = ['messageId', 'userId', 'authToken', 'readDel']
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
        message = Message.get_by_id(int(values["messageId"]))

        if message is None:
            write_error_to_response(self.response, {
                invalid_message_id['error']:
                    "Message doesn't exist with this message id"},
                                    invalid_message_id['status'])
            return

        if message.receiverId != int(values['userId']):
            write_error_to_response(self.response, {
                not_authorized['error']: "not authorized to edit this message"},
                                    not_authorized['status'])
            return

        if values["readDel"] in ["r", "R"]:
            #TODO: Not sure if we want to return error if message is already read
            message.received = True
            message.put()
        elif values["readDel"] in ["d", "D"]:
            message.key.delete()
        write_success_to_response(self.response, {})
