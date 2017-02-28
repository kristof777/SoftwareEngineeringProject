missing_province = {"error": "missingProvince", "status": 400}
missing_city = {"error": "missingCity", "status": 400}
missing_email = {"error": "missingEmail", "status": 400}
not_authorized = {"error": "notAuthorized", "status": 401}
email_alreadyExists = {"error": "emailAlreadyExists", "status": 403}
password_not_strong = {"error": "passwordNotStrong", "status": 403}
missing_confirmed_password = {"error": "missingConfirmedPassword","status": 400}
missing_first_name = {"error": "missingFirstName", "status": 400}
missing_last_name = {"error": "missingLastName", "status": 400}
missing_phone_number = {"error": "missingPhoneNumber", "status": 400}
missing_postal_code = {"error": "missingPostalCode", "status": 400}
nothing_requested_to_change = {"error": "nothingRequestedToChange","status":400}
missing_token = {"error": "missingToken", "status": 400}
unrecognized_key = {"error": "unrecognizedKey", "status": 403}
password_cant_be_changed = {"error": "passwordCantBeChanged", "status": 403}
invalid_user_id = {"error": "invalidUserId", "status": 403}
invalid_phone1 = {"error": "invalidPhone1", "status": 403}
invalid_phone2 = {"error": "invalidPhone2", "status": 403}
invalid_email = {"error": "invalidEmail", "status" :403}
missing_user_id = {"error": "missingUserId", "status": 400}
missing_password = {"error": "missingPassword", "status": 400}
missing_new_password = {"error": "missingNewPassword", "status": 400}
missing_new_password_confirmed = {"error": "missingNewPasswordConfirmed",
                                  "status": "400"}
no_favourite_listing = {"error": "noFavouriteListing", "status": 403}
invalid_listing_id = {"error": "invalidListingId", "status": 403}
missing_listing_id = {"error": "missingListingId", "status": 400}
missing_liked = {"error": "missingLiked", "status": 400}
duplicated_liked = {"error": "duplicatedLiked", "status": 403}
invalid_liked = {"error": "invalidLiked", "status": 403}
unallowed_liked = {"error": "unallowedLiked", "status": 403}
no_listings_left = {"error": "noListingsLeft", "status": 403}
missing_cursor = {"error": "missingCursor", "status": 400}
missing_last_listing_id = {"error": "missingLastListingId", "status": 400}
invalid_bedrooms = {"error": "invalidNumberOfBedrooms", "status": 403}
invalid_sqft = {"error":"invalidSquareFeet","status": 403}
invalid_bathrooms = {"error":"invalidNumberOfBathrooms", "status": 403}
invalid_price = {"error":"invalidPrice", "status": 403}
invalid_thumbnail_image_index = {"error":"invalidThumbnailImageIndex", "status": 403}
invalid_city = {"error": "invalidCity", "status": 403}
invalid_published = {"error": "invalidPublished", "status": 403}
invalid_province = {"error": "invalidProvince", "status": 403}
invalid_address = {"error": "invalidAddress", "status": 403}
missing_address = {"error": "missingAddress", "status": 400}
missing_price = {"error": "missingPrice", "status": 400}
missing_sqft = {"error": "missingSqft", "status": 400}
missing_bedrooms = {"error": "missingBedrooms", "status": 400}
missing_published = {"error": "missingPublished", "status": 400}
missing_bathrooms = {"error": "missingBathrooms", "status": 400}
missing_description = {"error": "missingDescription", "status": 400}
missing_image = {"error": "missingImage", "status": 400}
missing_image_index = {"error": "missingImageIndex", "status": 400}
un_auth_listing = {"error": "unAuthListing", "status": 401}
password_mismatch = {"error": "passwordMismatch", "status": 401}


invalids = {
    "phone1": invalid_phone1,
    "phone2": invalid_phone2,
    "email": invalid_email,
    "province": invalid_province,
    "password": password_not_strong,
    "listingId": invalid_listing_id,
    "userId": invalid_user_id,
    "price": invalid_price,
    "bedrooms": invalid_bedrooms,
    "bathrooms": invalid_bathrooms,
    "sqft": invalid_sqft,
    "isPublished": invalid_published,
    "thumbnailImageIndex": invalid_thumbnail_image_index,
    "liked": invalid_liked
}

missing = {

    "phone1": missing_phone_number,
    "email": missing_email,
    "password": missing_password,
    "confirmedPassword": missing_confirmed_password,
    "province": missing_province,
    "city": missing_city,
    "firstName": missing_first_name,
    "oldPassword": missing_password,
    "newPassword": missing_new_password,
    "newPasswordConfirmed": missing_new_password_confirmed,
    "changeValues": nothing_requested_to_change,
    "userId": missing_user_id,
    "authToken": missing_token,
    "listingId": missing_listing_id,
    "price": missing_price,
    "bedrooms": missing_bedrooms,
    "bathrooms": missing_bathrooms,
    "sqft": missing_sqft,
    "isPublished": missing_published,
    "thumbnailImageIndex": missing_image_index,
    "images": missing_image,
    "description": missing_description,
    "address": missing_address,
    "liked": missing_liked
}

missing_invalid_parameter_error = 400
unauthorized_access = 401
processing_failed = 403
success = 200
