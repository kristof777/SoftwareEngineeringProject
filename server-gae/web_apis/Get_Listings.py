from models.Listing import Listing
from models.User import User
from models.Favorite import Favorite
from extras.utils import *
import sys
sys.path.append("../")

DEFAULT_MAX_LIMIT = 20 # max number of listings required, by default (if not provided)
DEFAULT_UPPER = 100
DEFAULT_LOWER = 0

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
        # check validity for integer fields (userId, bedrooms, bathrooms, sqft, price, thumbnailImageIndex)
        #  and boolean field (isPublished)
        invalid = key_validation(values)
        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter_error)
            return

        invalid.update(is_valid_filter(values["filter"]) if "filter" in values else {})
        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter_error)
            return

        if not is_valid_xor(values, "listingIdList", "filter"):
            invalid[invalid_xor_condition['error']] = "ListingIdList and filter can't show up together"
            write_error_to_response(self.response, invalid, missing_invalid_parameter_error)
            return

        # Set default values
        # if max-limit = 100
        # if valuesRequired is not present = ["listingId"]
        #

        if "listingIdList" in values and not is_missing(values['listingIdList']):
            listingId_list = json.loads(values["listingIdList"])
            listing_info_list = []
            for listingId in listingId_list:

                listingId = int(listingId)
                listing_object = Listing.get_by_id(listingId)

                if listing_object is not None:
                    listing_info_list.append(create_returned_values_dict(listing_object, values))

            write_success_to_response(self.response, listing_info_list)
            return

        if "filter" in values and not is_missing(values["filter"]):

            filter = json.loads(values["filter"])

            # set default searchable listings to be all the listings
            filtered_listings = Listing.query().fetch()

            for key in filter:
                if key in ["bedrooms", "bathrooms", "sqft", "price", "bathrooms"]:
                    lower = DEFAULT_LOWER
                    upper = DEFAULT_UPPER
                    if "lower" in filter[key]:
                        lower = filter[key]["lower"]
                    if "upper" in filter[key]:
                        upper = filter[key]["upper"]
                    filtered_listings = Listing.query(Listing in filtered_listings,
                                                      Listing.get_value_from_key(key) >= lower,
                                                      Listing.get_value_from_key(key) <= upper).fetch()
                else: # not numeric key
                    filtered_listings = Listing.query(Listing in filtered_listings,
                                                      Listing.get_value_from_key(key) == filter[key]).fetch()

            # now filtered_listings contain all the listings that satisfy the filter conditions
            # we want to get listings that are not in favorites table (only if user signed in)
            # if user not sign in, we don't need to care about this favorite part
            if "userId" in values and not is_missing(values["userId"]):
                userId = int(json.loads(values["userId"]))
                favorites = Favorite.query(Favorite.userId == userId)
                seen_listings = []
                for favorite in favorites:
                    seen_listingId = favorite.listingId
                    seen_listing = Listing.get_by_id(seen_listingId)
                    if seen_listing is not None:
                        seen_listings.append(seen_listing)

                # now seenListings contains all the listings that are in the favorites table
                # we want the listings that are not in the favorite table
                filtered_listings = Listing.query(Listing not in seen_listings).fetch()
                # after this, filtered_listings contains all the listings that are not in the favorite table

            # now we want max number of items that haven't been seen to return
            maxLimit = DEFAULT_MAX_LIMIT

            if "maxLimit" in values and not is_missing(values["maxLimit"]):
                maxLimit = int(values["maxLimit"])

            if len(filtered_listings) >= maxLimit:
                filtered_listings = filtered_listings[0: maxLimit + 1]

            listing_info_list = []

            for listing_object in filtered_listings:
                if listing_object is not None:
                    listing_info_list.append(create_returned_values_dict(listing_object, values))

            write_success_to_response(self.response, listing_info_list)
            return


def create_returned_values_dict(listing_object, values_dict):
    listing_dict = {}
    if "valuesRequired" in values_dict and not is_missing(values_dict['valuesRequired']):
        # valuesRequired is not missing
        values_required = json.loads(values_dict["valuesRequired"])
        for key in values_required:
            listing_dict[key] = listing_object.get_value_from_key(key)
    else:
        # only returns listingIds
        listing_dict["listingId"] = listing_object.listingId

    return listing_dict












def is_valid_filter(filter):
    filter_object = json.loads(filter)
    if any(key not in ["sqft", "bedrooms", "bathrooms", "price", "city",
                       "province", "address", "description", "isPublished", "images",
                       "thumbnailImageIndex"] for key in filter_object):
        return unrecognized_key['error']
    for key in filter_object:
        if key in ["bedrooms", "bathrooms", "sqft", "price"]:
            if any(bound not in ["lower", "upper"] for bound in key):
                return invalid_filter_bound['error']
            invalid = {}
            if key == "bathrooms":
                if "lower" in filter[key]:
                    if not is_valid_float(filter[key]["lower"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom lower bound invalid"
                if "upper" in filter[key]:
                    if not is_valid_float(filter[key]["upper"]):
                        invalid[invalid_filter_bound['error']] = "Bathroom upper bound invalid"

            invalid.update(key_validation(filter[key]))
