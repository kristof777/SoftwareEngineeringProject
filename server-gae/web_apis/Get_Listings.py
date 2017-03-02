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
        errors, values = keys_missing({}, self.request.POST)

        invalid = key_validation(values)
        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter)
            return

        if "filter" in values:
            invalid.update(is_valid_filter(values["filter"]))
            if len(invalid) != 0:
                write_error_to_response(self.response, invalid, missing_invalid_parameter)
                return

        if not is_valid_xor(values, "listingIdList", "filter"):
            invalid[invalid_xor_condition['error']] = "ListingIdList and filter can't show up together"
            write_error_to_response(self.response, invalid, missing_invalid_parameter)
            return

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

        # set default value for upper and lower bounds
        bedrooms_max = DEFAULT_BEDROOMS_MAX
        bedrooms_min = DEFAULT_BEDROOMS_MIN
        bathrooms_max = DEFAULT_BATHROOMS_MAX
        bathrooms_min = DEFAULT_BATHROOMS_MIN
        sqft_max = DEFAULT_SQFT_MAX
        sqft_min = DEFAULT_SQFT_MIN
        price_max = DEFAULT_PRICE_MAX
        price_min = DEFAULT_PRICE_MIN
        non_numeric_dict = {}

        if "filter" in values and not is_empty(values["filter"]):

            filter = json.loads(values["filter"])

            for key in filter:
                if key in ["bedrooms", "sqft", "price", "bathrooms"]:
                    if key == "bedrooms":
                        if "lower" in filter[key]:
                            bedrooms_min = int(filter[key]["lower"])
                        if "upper" in filter[key]:
                            bedrooms_max = int(filter[key]["upper"])
                    elif key == "sqft":
                        if "lower" in filter[key]:
                            sqft_min = int(filter[key]["lower"])
                        if "upper" in filter[key]:
                            sqft_max = int(filter[key]["upper"])
                    elif key == "price":
                        if "lower" in filter[key]:
                            price_min = int(filter[key]["lower"])
                        if "upper" in filter[key]:
                            price_max = int(filter[key]["upper"])
                    elif key == "bathrooms":
                        if "lower" in filter[key]:
                            bathrooms_min = float(filter[key]["lower"])
                        if "upper" in filter[key]:
                            bathrooms_max = float(filter[key]["upper"])

                else: # not numeric key
                    if key == "province":
                        non_numeric_dict.update({"province": scale_province(filter[key])})
                    elif key == "city":
                        non_numeric_dict.update({"city": filter[key]})
                    elif key == "address":
                        non_numeric_dict.update({"address": filter[key]})
                    elif key == "isPublished":
                        non_numeric_dict.update({"isPublished": filter[key]})
                    elif key == "description":
                        non_numeric_dict.update({"description": filter[key]})


        # all numeric queries
        # google datastore doesn't allow more than two inequality conditions in one query, so creating multiple
        # queries and get their common set is the best option

        # query all the listings in db that satisfies the bedroom bound condition, only fetch their key(listingId)
        bedroom_query = Listing.query().filter(Listing.bedrooms >= bedrooms_min, Listing.bedrooms <= bedrooms_max)
        bedrooms_keys = bedroom_query.fetch(keys_only=True)
        bedrooms_keys_len = len(bedrooms_keys)

        # query all the listings in db that satisfies the sqft bound condition, only fetch their key(listingId)
        sqft_query = Listing.query().filter(Listing.sqft >= sqft_min, Listing.sqft <= sqft_max)
        sqft_keys = sqft_query.fetch(keys_only=True)
        sqft_keys_len = len(sqft_keys)

        # query all the listings in db that satisfies the price bound condition, only fetch their key(listingId)
        price_query = Listing.query().filter(Listing.price >= price_min, Listing.price <= price_max)
        price_keys = price_query.fetch(keys_only=True)
        price_keys_len = len(price_keys)

        # query all the listings in db that satisfies the price bound condition, only fetch their key(listingId)
        bathrooms_query = Listing.query().filter(Listing.bathrooms >= bathrooms_min, Listing.bathrooms <= bathrooms_max)
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

        # Get the common set of the two key(listingId) sets from above, this is the final common set we need
        final_valid_keys = list(set(valid_bd_sqft_keys) & set(valid_bt_pr_keys))
        assert len(final_valid_keys) == min(bd_sqft_keys_len, bt_pr_keys_len)

        returned_listing_ids = []

        # check un_numeric_fields
        for key in final_valid_keys:
            listingId = key.id()
            listing = Listing.get_by_id(listingId)
            matched = True
            for field in non_numeric_dict:
                if listing.get_value_from_key(field) != non_numeric_dict[field]:
                    matched = False
                    break
            if matched:
                returned_listing_ids.append(listing.listingId)

        # so returned_listings contains all the listings that fits the filter..omg

        # now returned_listings contain all the listings that satisfy the filter conditions
        # we want to get listings that are not in favorites table (only if user signed in)
        # if user not sign in, we don't need to care about this favorite part
        if "userId" in values and not is_empty(values["userId"]):
            userId = int(json.loads(values["userId"]))
            favorites = Favorite.query(Favorite.userId == userId).fetch()
            seen_listing_ids = []
            for favorite in favorites:
                seen_listingId = favorite.listingId
                seen_listing = Listing.get_by_id(seen_listingId)
                if seen_listing is not None:
                    seen_listing_ids.append(seen_listing.listingId)

            # now seenListingIds contains all the listings' ids that are in the favorites table
            # we want the listings that are not in the favorite table
            # so we have returned_listing_ids which contains the superset of listingIds,
            # we wanna delete those listingIds which are in the seen_listing_ids
            filtered_listing_ids = returned_listing_ids
            for seen_listing_id in seen_listing_ids:
                if seen_listing_id in returned_listing_ids:
                    filtered_listing_ids.remove(seen_listing_id)

            returned_listing_ids = filtered_listing_ids

        # after this, returned_listing_ids contains all the listings' ids that
        # are satisfying filter conditions and not in the favorite table

        # now we want max number of items that haven't been seen to return
        maxLimit = DEFAULT_MAX_LIMIT

        if "maxLimit" in values and not is_empty(values["maxLimit"]):
            maxLimit = int(values["maxLimit"])

        if len(returned_listing_ids) >= maxLimit:
            returned_listing_ids = returned_listing_ids[0: maxLimit + 1]

        listing_info_list = []

        for listing_object_id in returned_listing_ids:
            listing_object = Listing.get_by_id(listing_object_id)
            if listing_object is not None:
                listing_info_list.append(create_returned_values_dict(listing_object, values))

        write_success_to_response(self.response, listing_info_list)


def create_returned_values_dict(listing_object, values_dict):
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


def is_valid_filter(filter):
    if len(filter) == 0:
        return {}

    filter = json.loads(filter)
    invalid = {}

    for key in filter:
        if key not in ["sqft", "bedrooms", "bathrooms", "price", "city",
                       "province", "address", "description", "isPublished", "images",
                       "thumbnailImageIndex"]:
            invalid[unrecognized_key['error']] = "Unrecognized key " + key
            break
        if key in ["bedrooms", "bathrooms", "sqft", "price"]:
            if any(bound not in ["lower", "upper"] for bound in filter[key]):
                invalid[invalid_filter_bound['error']] = str(key) + " upper/lower bound invalid"
                break
            if key == "bathrooms":
                if "lower" in filter[key]:
                    if not is_valid_float(filter[key]["lower"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom lower bound invalid"
                if "upper" in filter[key]:
                    if not is_valid_float(filter[key]["upper"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom upper bound invalid"

            invalid.update(key_validation(filter[key]))

    return invalid
