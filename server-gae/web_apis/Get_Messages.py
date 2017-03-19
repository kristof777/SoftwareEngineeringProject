import sys
from extras.Utils import *
from models.Listing import Listing
from models.Message import Message
from models.User import User
from API_NAME import get_messages_api
from extras.Required_Fields import check_required_valid
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
        setup_api_options(self)

    def get(self):
        self.response.out.write()

    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(get_messages_api, self.request.POST,
                                 self.response, True)

        if not valid:
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































