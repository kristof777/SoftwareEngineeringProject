from Error_Code import *
from API_NAME import *
import utils
from models.User import User

"""
    Creates a dictionary with all fields that are required per API call
"""

required_api_dict = {
    sign_in_api: ['email', 'password'],
    create_user_api: ['email', 'firstName', 'password', 'confirmedPassword',
                      'phone1', 'province', 'city'],
    change_password_api: ['oldPassword', 'newPassword', 'confirmedPassword',
                          'userId'],
    contact_seller_api: ['senderId', 'listingId', 'message', 'phone',
                         'email', 'authToken', 'receiverId'],
    create_listing_api: ["isPublished", "userId", "authToken"],
    delete_listing_api: ['userId', 'listingId', 'authToken'],
    edit_listing_api: ['changeValues', 'userId', 'listingId', 'authToken'],
    edit_message_api: ['messageId', 'userId', 'authToken', 'readDel'],
    edit_user_api: ['changeValues', 'userId', 'authToken'],
    fb_login_api: ['fbId'],
    get_favourites_listing_api: ['userId', 'authToken'],
    get_listing_api: [],
    get_messages_api: ['userId', 'authToken'],
    get_my_listings_api: ['userId', 'authToken'],
    like_listing_api: ['userId', 'listingId', 'liked', 'authToken'],
    sign_in_token_api: ['authToken', 'userId'],
    sign_out_api: ['userId', 'authToken']
}


def check_required_valid(api, post, response, auth_required=False):
    # TODO Complete this spec, Gaurav
    """
    TODO
    :param api:
    :param post:
    :param response:
    :param auth_required:
    :return:
    """
    # validating if request has all required key
    errors, values = utils.keys_missing(required_api_dict[api], post)

    # If there exists error then return the response, and stop the function
    if len(errors) > 0:
        utils.write_error_to_response(response, errors,
                                      missing_invalid_parameter)
        return False, None

    invalid = utils.key_validation(values)

    # If there exists an invalidation, return null and stop the function
    if len(invalid) > 0:
        utils.write_error_to_response(response, invalid,
                                      missing_invalid_parameter)
        return False, None

    assert len(errors) == 0
    assert len(invalid) == 0

    if auth_required:
        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'User not authorized'
            }
            utils.write_error_to_response(response, error,
                                          not_authorized["status"])
            return False, None

        valid_user = user.validate_token(int(values["userId"]),
                                         "auth", values["authToken"])

        if not valid_user:
            utils.write_error_to_response(response, {not_authorized['error']: "not authorized to create listings"},
                                          not_authorized['status'])
            return False, None

        assert valid_user
        assert user is not None

    assert len(errors) == 0
    assert len(invalid) == 0

    return True, values
