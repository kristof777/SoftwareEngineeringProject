from google.appengine.ext import ndb

from models.Listing import Listing
from models.User import User
from models.Favorite import Favorite
from extras.utils import *
import sys
sys.path.append("../")

DEFAULT_MAX_LIMIT = 20 # max number of listings required, by default (if not provided)


class GetListing(webapp2.RequestHandler):
    """
    Class used to handle get filtered listings.
    Get:  do nothing
    Post:
        @pre-cond: all keys are optional
        @post-cond: get all listings that match the filter back as response
    """
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        # every field (userId, valuesRequired, filter) is optional
        errors, values = keys_missing({}, self.request.POST)
        print self.request.POST
        invalid = key_validation(values)
        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter)
            return

        if "filter" in values:
            invalid.update(is_valid_filter(values["filter"]))
            if len(invalid) != 0:
                write_error_to_response(self.response, invalid, missing_invalid_parameter)
                return

        # make sure that "listingIdList" and "filter" fields are not being passed in in the request
        if not is_valid_xor(values, "listingIdList", "filter"):
            invalid[invalid_xor_condition['error']] = "ListingIdList and filter can't show up together"
            write_error_to_response(self.response, invalid, missing_invalid_parameter)
            return

        # This part should never be called
        if is_existing_and_non_empty("listingIdList", values):
            listing_info_list = get_listings_from_listing_ids(values)
            write_success_to_response(self.response, listing_info_list)
            return

        # Now time to deal with the filter

        non_numeric_dict = {}

        # if the filter does exist and is not empty, then we decode the conditions in it,
        # if it doesn't exist, we use the default filter
        if is_existing_and_non_empty("filter", values):
            non_numeric_dict = decode_filter(values["filter"])

        # Now, send queries with all numeric bounds
        final_valid_keys = get_listingIds_with_numeric_bounds()

        # check un_numeric_fields
        returned_listing_ids = []

        for key in final_valid_keys:
            listing_id = key.id()
            listing = Listing.get_by_id(listing_id)
            matched = True
            for field in non_numeric_dict:
                if listing.get_value_from_key(field) != non_numeric_dict[field]:
                    matched = False
                    break
            if matched:
                returned_listing_ids.append(listing.listingId)

        # we want to get listings that are not in favorites table (only if user signed in)
        # if user not sign in, we don't need to care about this favorite part
        if is_existing_and_non_empty("userId", values):
            user = User.get_by_id(int(values['userId']))
            if user is None:
                error = {
                    not_authorized['error']: 'User not authorized'
                }
                write_error_to_response(self.response, error, unauthorized_access)
                return
            if not is_existing_and_non_empty("authToken", values):
                error = {
                    missing_token['error']: 'AuthToken is missing'
                }
                write_error_to_response(self.response, error, unauthorized_access)
                return

            # Check if it is the valid user
            valid_user = user.validate_token(int(values["userId"]),
                                             "auth",
                                             values["authToken"])
            if not valid_user:
                write_error_to_response(self.response, {not_authorized['error']:
                                                            "not authorized to get filtered listings"},
                                        not_authorized['status'])
                return

            returned_listing_ids = filter_favorite_listings(values["userId"], returned_listing_ids)

        # now we decide the number of items to  return
        max_limit = DEFAULT_MAX_LIMIT

        if is_existing_and_non_empty("maxLimit", values):
            max_limit = int(values["maxLimit"])
        # if the number of listings we have filtered is greater than or equal to the max limit,
        # then return max_limit number of listings. If not, return all filtered listings
        if len(returned_listing_ids) >= max_limit:
            returned_listing_ids = returned_listing_ids[0: max_limit + 1]

        listing_info_list = []

        for listing_object_id in returned_listing_ids:
            listing_object = Listing.get_by_id(listing_object_id)
            if listing_object is not None:
                listing_info_list.append(create_returned_values_dict(listing_object, values))

        Listing.reset_filter()
        write_success_to_response(self.response, listing_info_list)


def create_returned_values_dict(listing_object, values_dict):
    """
    This function is to get the returned fields that the request declared in field "valuesRequired"

    @pre-cond: none
    @post-cond: none

    :param listing_object: the Listing object
    :param values_dict: the request data
    :return the dictionary of returned data for that listing
    """
    listing_dict = {}
    if is_existing_and_non_empty("valuesRequired", values_dict):
        values_required = json.loads(values_dict["valuesRequired"])
        for key in values_required:
            listing_dict[key] = listing_object.get_value_from_key(key)
    else:
        # only returns listingIds
        listing_dict["listingId"] = listing_object.listingId

    return listing_dict


def is_valid_filter(filter_json):
    """
    This function is checking if the data in the "filter" dictionary are valid,
    that means each key in filter dictionary is in the list ["address", "bedrooms"...]
    And if the key is one of numeric fields ["bathrooms", "sqft", "bedrooms", "price"],
    we check if there is an inner dictionary whose keys are in the bound list ["upper", "lower"]

    @pre-cond: none
    @post-cond: none

    :param "filterJson" json object in the "filter" field from the request
    :return the dictionary that contains invalid errors, empty if everything is valid
    """

    if len(filter_json) == 0:
        return {}

    filter_object = json.loads(filter_json)
    invalid = {}

    for key in filter_object:
        if key not in ["squarefeet", "bedrooms", "bathrooms", "price", "city",
                       "province", "address", "description", "isPublished", "images",
                       "thumbnailImageIndex"]:
            invalid[unrecognized_key['error']] = "Unrecognized key " + key
            break
        if key in ["bedrooms", "bathrooms", "squarefeet", "price"]:
            if any(bound not in ["lower", "upper"] for bound in filter_object[key]):
                invalid[invalid_filter_bound['error']] = str(key) + " upper/lower bound invalid"
                break
            if key == "bathrooms":
                if "lower" in filter_object[key]:
                    if not is_valid_float(filter_object[key]["lower"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom lower bound invalid"
                if "upper" in filter_object[key]:
                    if not is_valid_float(filter_object[key]["upper"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom upper bound invalid"

            invalid.update(key_validation(filter_object[key]))

    return invalid


def decode_filter(filter_json):
    """
    This function is for decoding everything in the "filter" field
    For numeric conditions, if there's "upper" or "lower" bounds,
    replace the default bounds with the sent ones.
    For non-numeric conditions, simply add the key-value to the non_numeric dictionary

    @pre-cond: none
    @post-cond: none

    :param "filterJson" json object in the "filter" field from the request
    :return the non_numeric dictionary that contains all non_numeric key-value pairs
    """

    filter_object = json.loads(filter_json)
    non_numeric_dict = {}

    for key in filter_object:
        if key in ["bedrooms", "squarefeet", "price", "bathrooms"]:  # if key is a numeric field
            if key == "bedrooms":
                if "lower" in filter_object[key]:
                    Listing.numeric_filter_bounds['bedrooms_min'] = int(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    Listing.numeric_filter_bounds['bedrooms_max'] = int(filter_object[key]["upper"])
            elif key == "squarefeet":
                if "lower" in filter_object[key]:
                    Listing.numeric_filter_bounds['sqft_min'] = int(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    Listing.numeric_filter_bounds['sqft_max'] = int(filter_object[key]["upper"])
            elif key == "price":
                if "lower" in filter_object[key]:
                    Listing.numeric_filter_bounds['price_min'] = int(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    Listing.numeric_filter_bounds['price_max'] = int(filter_object[key]["upper"])
            elif key == "bathrooms":
                if "lower" in filter_object[key]:
                    Listing.numeric_filter_bounds['bathrooms_min'] = float(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    Listing.numeric_filter_bounds['bathrooms_max'] = float(filter_object[key]["upper"])

        else:
            if key == "province":
                non_numeric_dict["province"] = scale_province(filter_object[key])
            else:
                non_numeric_dict[key] = filter_object[key]

    return non_numeric_dict


def get_listingIds_with_numeric_bounds():
    """
    This function is for getting the filtered listing_ids that satisfies all
    numeric bounds

    @pre-cond: none
    @post-cond: none

    :return the list of filtered listingIds
    """

    # google datastore doesn't allow more than one inequality conditions in one query
    # so what is done here is creating four separate queries in all listings in db and
    # and get the common set from those four queries

    # query all the listings in db that satisfies the bedroom bound condition,
    # only fetch their key(listingId) for efficiency
    bedroom_query = Listing.query().filter(Listing.bedrooms >= Listing.numeric_filter_bounds['bedrooms_min'],
                                           Listing.bedrooms <= Listing.numeric_filter_bounds['bedrooms_max'])
    bedrooms_keys = bedroom_query.fetch(keys_only=True)
    bedrooms_keys_len = len(bedrooms_keys)

    # query all the listings in db that satisfies the sqft bound condition,
    # only fetch their key(listingId) for efficiency
    sqft_query = Listing.query().filter(Listing.squarefeet >= Listing.numeric_filter_bounds['sqft_min'],
                                        Listing.squarefeet <= Listing.numeric_filter_bounds['sqft_max'])
    sqft_keys = sqft_query.fetch(keys_only=True)
    sqft_keys_len = len(sqft_keys)

    # query all the listings in db that satisfies the price bound condition
    # only fetch their key(listingId) for efficiency
    price_query = Listing.query().filter(Listing.price >= Listing.numeric_filter_bounds['price_min'],
                                         Listing.price <= Listing.numeric_filter_bounds['price_max'])
    price_keys = price_query.fetch(keys_only=True)
    price_keys_len = len(price_keys)

    # query all the listings in db that satisfies the price bound condition
    # only fetch their key(listingId) for efficiency
    bathrooms_query = Listing.query().filter(Listing.bathrooms >= Listing.numeric_filter_bounds['bathrooms_min'],
                                             Listing.bathrooms <= Listing.numeric_filter_bounds['bathrooms_max'])
    bathrooms_keys = bathrooms_query.fetch(keys_only=True)
    bathrooms_keys_len = len(bathrooms_keys)

    # Get the common set of the first two key(listingId) sets
    valid_bd_sqft_keys = list(set(bedrooms_keys) & set(sqft_keys))
    # assert len(valid_bd_sqft_keys) == min(bedrooms_keys_len, sqft_keys_len)
    bd_sqft_keys_len = len(valid_bd_sqft_keys)

    # Get the common set of the next two key(listingId) sets
    valid_bt_pr_keys = list(set(price_keys) & set(bathrooms_keys))
    assert len(valid_bt_pr_keys) == min(price_keys_len, bathrooms_keys_len)
    bt_pr_keys_len = len(valid_bt_pr_keys)

    # Get the common set of the two key(listingId) sets above, this is the final common set we need
    final_valid_keys = list(set(valid_bd_sqft_keys) & set(valid_bt_pr_keys))
    assert len(final_valid_keys) == min(bd_sqft_keys_len, bt_pr_keys_len)

    return final_valid_keys


def filter_favorite_listings(user_id, listing_ids):
    """
    This function is removing all favorite listings that are in the filtered listings

    @pre-cond: user_id and listing_ids are not none
    @post-cond: none

    :parameter user_id: the userId in order to find all his/her favorites
    :parameter listing_ids: the list of listingIds
    :return the list of listingIds after this filter
    """

    user_id = int(json.loads(user_id))
    favorites = Favorite.query(Favorite.userId == user_id).fetch()
    seen_listing_ids = []
    for favorite in favorites:
        seen_listing_id = favorite.listingId
        seen_listing = Listing.get_by_id(seen_listing_id)
        if seen_listing is not None:
            seen_listing_ids.append(seen_listing.listingId)

    # wanna delete those listingIds which are in the seen_listing_ids
    filtered_listing_ids = listing_ids
    for seen_listing_id in seen_listing_ids:
        if seen_listing_id in listing_ids:
            filtered_listing_ids.remove(seen_listing_id)

    return filtered_listing_ids


def get_listings_from_listing_ids(values):
    """
    This function is get a list of listings from listingIds

    @pre-cond: values["listingIdList"] is not empty
    @post-cond: none

    :parameter values: the request object
    :return the list of listings
    """
    listing_id_list = json.loads(values["listingIdList"])
    listing_info_list = []
    for listingId in listing_id_list:
        listing_object = Listing.get_by_id(int(listingId))

        if listing_object is not None:
            listing_info_list.append(create_returned_values_dict(listing_object, values))

    return listing_info_list
