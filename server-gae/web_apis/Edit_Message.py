import sys
from extras.utils import *
from models.Message import Message
from models.User import User
from API_NAME import edit_message_api
from extras.api_required_fields import check_required_valid

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
        valid, values = \
            check_required_valid(edit_message_api, self.request.POST,
                                 self.response, True)

        if not valid:
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
            message.received = True
            message.put()
        elif values["readDel"] in ["d", "D"]:
            message.key.delete()
        write_success_to_response(self.response, {})
