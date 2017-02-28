import json
import os
import sys
sys.path.append("../")
import webapp2
import extras.Error_Code as Error_Code
from models.Listing import Listing

class GetMyListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        errors = {}
        emptyData = u''

        ownerId = self.request.POST.get('userId')
        if ownerId is emptyData or ownerId is None or ownerId.isspace():
            errors[Error_Code.missing_user_id['error']] = "UserId not provided"
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        try:
            ownerId = int(ownerId)
        except:
            errors[Error_Code.invalid_user_id['error']] = "UserId not valid"
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        myListings = Listing.query(Listing.userId == ownerId).fetch()
        returnedArray = []

        for listing in myListings:
            template_values = {
                'listingId': listing.listingId,
                'userId': listing.userId,
                'bedrooms': listing.bedrooms,
                'sqft': listing.sqft,
                'bathrooms': listing.bathrooms,
                'price': listing.price,
                'description': listing.description,
                'isPublished': listing.isPublished,
                'province': listing.province,
                'city': listing.city,
                'address': listing.address,
                'images': listing.images,
                'thumbnailImageIndex': listing.thumbnailImageIndex
            }
            returnedArray.append(template_values)

        self.response.write(json.dumps({"myListings": returnedArray}))
        self.response.set_status(Error_Code.success)






