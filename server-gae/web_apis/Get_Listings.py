from google.appengine.ext import ndb

from models.Listing import Listing
from models.User import User
from models.Favorite import Favorite
from extras.utils import *
import sys
sys.path.append("../")

DEFAULT_MAX_LIMIT = 20 # max number of listings required, by default (if not provided)

DEFAULT_BEDROOMS_MAX = 10
DEFAULT_BEDROOMS_MIN = 1
DEFAULT_BATHROOMS_MAX = 10.0
DEFAULT_BATHROOMS_MIN = 1.0
DEFAULT_SQFT_MAX = 10000
DEFAULT_SQFT_MIN = 0
DEFAULT_PRICE_MAX = 999999999
DEFAULT_PRICE_MIN = 10

# Set default value for upper and lower bounds
BEDROOM_MAX = DEFAULT_BEDROOMS_MAX
BEDROOM_MIN = DEFAULT_BEDROOMS_MIN
BATHROOM_MAX = DEFAULT_BATHROOMS_MAX
BATHROOM_MIN = DEFAULT_BATHROOMS_MIN
SQFT_MAX = DEFAULT_SQFT_MAX
SQFT_MIN = DEFAULT_SQFT_MIN
PRICE_MAX = DEFAULT_PRICE_MAX
PRICE_MIN = DEFAULT_PRICE_MIN

class GetListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        # Since every field (userId, valuesRequired, filter) are optional, so it's fine if any of these is missing
        # That's why we leave the missing_key dictionary empty
        errors, values = keys_missing({}, self.request.POST)

        # check if valuesRequired contains any invalid/unrecognized elements
        # every element should be one of [price, bathrooms, bedrooms,...]
        invalid = key_validation(values)
        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter)
            return

        # if we have a "filter" field passed in
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

        # This part should never be called since the listings are not gonna be stored on devices
        # But it's here just in case
        if "listingIdList" in values and not is_empty(values['listingIdList']):
            listingId_list = json.loads(values["listingIdList"])
            listing_info_list = []
            for listingId in listingId_list:

                listingId = int(listingId)
                listing_object = Listing.get_by_id(listingId)

                if listing_object is not None:
                    listing_info_list.append(create_returned_values_dict(listing_object, values))

            write_success_to_response(self.response, listing_info_list)
            return

        # Now time to deal with the filter

        # if there's non-numeric field in the filter (such as "city", "address", "description",
        # make sure to store it in a dictionary when we decode them, which is initialized to be empty
        non_numeric_dict = {}

        # if the filter does exist and is not empty, then we decode the conditions in it,
        # if it doesn't exist, we use the default filter
        if "filter" in values and not is_empty(values["filter"]):
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

        # now returned_listings contain all the listings that satisfy the filter conditions

        # we want to get listings that are not in favorites table (only if user signed in)
        # if user not sign in, we don't need to care about this favorite part
        if "userId" in values and not is_empty(values["userId"]):
            returned_listing_ids = filter_favorite_listings(values["userId"], returned_listing_ids)

        # after this, returned_listing_ids contains all the listings' ids that
        # are satisfying filter conditions and not in the favorite table

        # now we decide the number of items to  return
        max_limit = DEFAULT_MAX_LIMIT

        # if max_limit is provided by the request
        if "maxLimit" in values and not is_empty(values["maxLimit"]):
            max_limit = int(values["maxLimit"])
        # if the number of listings we have filtered is greater than or equal to the max limit,
        # then return max_limit number of listings. If not, return all filtered listings
        if len(returned_listing_ids) >= max_limit:
            returned_listing_ids = returned_listing_ids[0: max_limit + 1]

        # now we decide which field to return according to the "valueRequired" in the request
        # if not provided, then only return a list of listingIds
        listing_info_list = []

        for listing_object_id in returned_listing_ids:
            listing_object = Listing.get_by_id(listing_object_id)
            if listing_object is not None:
                listing_info_list.append(create_returned_values_dict(listing_object, values))

        write_success_to_response(self.response, listing_info_list)


def create_returned_values_dict(listing_object, values_dict):
    """
    This function is to get the returned fields that the request declared in field "valuesRequired"

    :param listing_object: the Listing object
    :param values_dict: the request data
    :return the dictionary of returned data for that listing
    """
    listing_dict = {}
    if "valuesRequired" in values_dict and not is_empty(values_dict['valuesRequired']):
        # valuesRequired is not missing
        values_required = json.loads(values_dict["valuesRequired"])
        for key in values_required:
            listing_dict[key] = listing_object.get_value_from_key(key)
    else:
        # only returns listingIds
        listing_dict["listingId"] = listing_object.listingId

    return listing_dict


def is_valid_filter(filterJson):
    """
    This function is checking if the data in the "filter" dictionary are valid,
    that means each key in filter dictionary is in the list ["address", "bedrooms"...]
    And if the key is one of numeric fields ["bathrooms", "sqft", "bedrooms", "price"],
    we check if there is an inner dictionary whose keys are in the bound list ["upper", "lower"]

    :param "filterJson" json object in the "filter" field from the request
    :return the dictionary that contains invalid errors, empty if everything is valid
    """

    if len(filterJson) == 0:
        return {}

    filterObject = json.loads(filterJson)
    invalid = {}

    for key in filterObject:
        if key not in ["sqft", "bedrooms", "bathrooms", "price", "city",
                       "province", "address", "description", "isPublished", "images",
                       "thumbnailImageIndex"]:
            invalid[unrecognized_key['error']] = "Unrecognized key " + key
            break
        if key in ["bedrooms", "bathrooms", "sqft", "price"]:
            if any(bound not in ["lower", "upper"] for bound in filterObject[key]):
                invalid[invalid_filter_bound['error']] = str(key) + " upper/lower bound invalid"
                break
            if key == "bathrooms":
                if "lower" in filterObject[key]:
                    if not is_valid_float(filterObject[key]["lower"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom lower bound invalid"
                if "upper" in filterObject[key]:
                    if not is_valid_float(filterObject[key]["upper"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom upper bound invalid"

            invalid.update(key_validation(filterObject[key]))

    return invalid


def decode_filter(filterJson):
    """
    This function is for decoding everything in the "filter" field
    For numeric conditions, if there's "upper" or "lower" bounds,
    replace the default bounds with the sent ones.
    For non-numeric conditions, simply add the key-value to the non_numeric dictionary

    :param "filterJson" json object in the "filter" field from the request
    :return the non_numeric dictionary that contains all non_numeric key-value pairs
    """

    filter_object = json.loads(filterJson)
    non_numeric_dict = {}

    global BEDROOM_MAX, BEDROOM_MIN, SQFT_MAX, SQFT_MIN
    global PRICE_MIN, PRICE_MAX, BATHROOM_MIN, BATHROOM_MAX

    for key in filter_object:
        if key in ["bedrooms", "sqft", "price", "bathrooms"]:  # if key is a numeric field
            if key == "bedrooms":
                # check if "lower" and "upper" are specified
                if "lower" in filter_object[key]:
                    BEDROOM_MIN = int(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    BEDROOM_MAX = int(filter_object[key]["upper"])
            elif key == "sqft":
                # check if "lower" and "upper" are specified
                if "lower" in filter_object[key]:
                    SQFT_MIN = int(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    SQFT_MAX = int(filter_object[key]["upper"])
            elif key == "price":
                # check if "lower" and "upper" are specified
                if "lower" in filter_object[key]:
                    PRICE_MIN = int(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    PRICE_MAX = int(filter_object[key]["upper"])
            elif key == "bathrooms":
                # check if "lower" and "upper" are specified
                if "lower" in filter_object[key]:
                    BATHROOM_MIN = float(filter_object[key]["lower"])
                if "upper" in filter_object[key]:
                    BATHROOM_MAX = float(filter_object[key]["upper"])

        else:  # if key is not numeric
            if key == "province":
                # if the user send "saskatchewan", we need to scale it to "SK",
                # and store this key-value pair into non_numeric dictionary
                non_numeric_dict.update({"province": scale_province(filter_object[key])})
            else:
                # directly store this key-value pair into non_numeric dictionary
                non_numeric_dict.update({key: filter_object[key]})

    return non_numeric_dict


def get_listingIds_with_numeric_bounds():
    """
    This function is for getting the filtered listing_ids that satisfies all
    numeric bounds

    :return the list of filtered listingIds
    """

    # google datastore doesn't allow more than one inequality conditions in one query
    # so what is done here is creating four separate queries in all listings in db and
    # and get the common set from those four queries

    # query all the listings in db that satisfies the bedroom bound condition,
    # only fetch their key(listingId) for efficiency
    bedroom_query = Listing.query().filter(Listing.bedrooms >= BEDROOM_MIN, Listing.bedrooms <= BEDROOM_MAX)
    bedrooms_keys = bedroom_query.fetch(keys_only=True)
    bedrooms_keys_len = len(bedrooms_keys)

    # query all the listings in db that satisfies the sqft bound condition,
    # only fetch their key(listingId) for efficiency
    sqft_query = Listing.query().filter(Listing.sqft >= SQFT_MIN, Listing.sqft <= SQFT_MAX)
    sqft_keys = sqft_query.fetch(keys_only=True)
    sqft_keys_len = len(sqft_keys)

    # query all the listings in db that satisfies the price bound condition
    # only fetch their key(listingId) for efficiency
    price_query = Listing.query().filter(Listing.price >= PRICE_MIN, Listing.price <= PRICE_MAX)
    price_keys = price_query.fetch(keys_only=True)
    price_keys_len = len(price_keys)

    # query all the listings in db that satisfies the price bound condition
    # only fetch their key(listingId) for efficiency
    bathrooms_query = Listing.query().filter(Listing.bathrooms >= BATHROOM_MIN, Listing.bathrooms <= BATHROOM_MAX)
    bathrooms_keys = bathrooms_query.fetch(keys_only=True)
    bathrooms_keys_len = len(bathrooms_keys)

    # Get the common set of the first two key(listingId) sets
    valid_bd_sqft_keys = list(set(bedrooms_keys) & set(sqft_keys))
    assert len(valid_bd_sqft_keys) == min(bedrooms_keys_len, sqft_keys_len)
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

    # now seenListingIds contains all the listings' ids that are in the favorites table
    # we want the listings that are not in the favorite table
    # so we have returned_listing_ids which contains the superset of listingIds,
    # we wanna delete those listingIds which are in the seen_listing_ids
    filtered_listing_ids = listing_ids
    for seen_listing_id in seen_listing_ids:
        if seen_listing_id in listing_ids:
            filtered_listing_ids.remove(seen_listing_id)

    return filtered_listing_ids
