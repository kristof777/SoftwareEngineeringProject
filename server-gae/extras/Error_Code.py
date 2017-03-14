missing_invalid_parameter = 400
unauthorized_access = 401
processing_failed = 403
success = 200
missing_province = {"error": "missingProvince",
                    "status": missing_invalid_parameter}

missing_city = {"error": "missingCity",
                "status": missing_invalid_parameter}

missing_email = {"error": "missingEmail",
                 "status": missing_invalid_parameter}

not_authorized = {"error": "notAuthorized",
                  "status": unauthorized_access}

email_alreadyExists = {"error": "emailAlreadyExists",
                       "status": processing_failed}

password_not_strong = {"error": "passwordNotStrong",
                       "status": processing_failed}

missing_confirmed_password = {"error": "missingConfirmedPassword",
                              "status": missing_invalid_parameter}

missing_first_name = {"error": "missingFirstName",
                      "status": missing_invalid_parameter}

missing_last_name = {"error": "missingLastName",
                     "status": missing_invalid_parameter}

missing_phone_number = {"error": "missingPhoneNumber",
                        "status": missing_invalid_parameter}

missing_postal_code = {"error": "missingPostalCode",
                       "status": missing_invalid_parameter}

nothing_requested_to_change = {"error": "nothingRequestedToChange",
                               "status": processing_failed}

missing_token = {"error": "missingToken",
                 "status": unauthorized_access}

unrecognized_key = {"error": "unrecognizedKey",
                    "status": processing_failed}

password_cant_be_changed = {"error": "passwordCantBeChanged",
                            "status": processing_failed}

new_password_is_the_same_as_old = {"error": "newPasswordIsTheSameAsOld",
                            "status": processing_failed}

invalid_user_id = {"error": "invalidUserId",
                   "status": missing_invalid_parameter}

invalid_phone1 = {"error": "invalidPhone1",
                  "status": missing_invalid_parameter}

invalid_phone2 = {"error": "invalidPhone2",
                  "status": missing_invalid_parameter}

invalid_phone = {"error": "invalidPhone",
                 "status": missing_invalid_parameter}

invalid_email = {"error": "invalidEmail",
                 "status": missing_invalid_parameter}

missing_user_id = {"error": "missingUserId",
                   "status": missing_invalid_parameter}

missing_password = {"error": "missingPassword",
                    "status": missing_invalid_parameter}

missing_new_password = {"error": "missingNewPassword",
                        "status": missing_invalid_parameter}

missing_new_password_confirmed = {"error": "missingNewPasswordConfirmed",
                                  "status": missing_invalid_parameter}

no_favourite_listing = {"error": "noFavouriteListing",
                        "status": processing_failed}

invalid_listing_id = {"error": "invalidListingId",
                      "status": missing_invalid_parameter}

missing_listing_id = {"error": "missingListingId",
                      "status": missing_invalid_parameter}

invalid_images = {"error": "invalidImages",
                  "status": missing_invalid_parameter}

missing_liked = {"error": "missingLiked",
                 "status": missing_invalid_parameter}

duplicated_liked = {"error": "duplicatedLiked",
                    "status": processing_failed}

invalid_liked = {"error": "invalidLiked",
                 "status": missing_invalid_parameter}

unallowed_liked = {"error": "unallowedLiked",
                   "status": processing_failed}

no_listings_left = {"error": "noListingsLeft",
                    "status": processing_failed}

invalid_bedrooms = {"error": "invalidNumberOfBedrooms",
                    "status": missing_invalid_parameter}

invalid_squarefeet = {"error": "invalidSquareFeet",
                "status": missing_invalid_parameter}

invalid_bathrooms = {"error": "invalidNumberOfBathrooms",
                     "status": missing_invalid_parameter}

invalid_price = {"error": "invalidPrice",
                 "status": missing_invalid_parameter}

invalid_thumbnail_image_index = {"error": "invalidThumbnailImageIndex",
                                 "status": missing_invalid_parameter}

invalid_city = {"error": "invalidCity",
                "status": missing_invalid_parameter}

invalid_published = {"error": "invalidPublished",
                     "status": missing_invalid_parameter}

invalid_province = {"error": "invalidProvince",
                    "status": missing_invalid_parameter}

invalid_address = {"error": "invalidAddress",
                   "status": missing_invalid_parameter}

invalid_filter_bound = {"error": "invalidFilterBound",
                        "status": missing_invalid_parameter}

invalid_longitude = {"error": "invalidLongitude",
                     "status": missing_invalid_parameter}

invalid_latitude = {"error": "invalidLatitude",
                    "status": missing_invalid_parameter}

missing_address = {"error": "missingAddress",
                   "status": missing_invalid_parameter}

missing_price = {"error": "missingPrice",
                 "status": missing_invalid_parameter}

missing_squarefeet = {"error": "missingSqft",
                "status": missing_invalid_parameter}

missing_bedrooms = {"error": "missingBedrooms",
                    "status": missing_invalid_parameter}

missing_published = {"error": "missingPublished",
                     "status": missing_invalid_parameter}

missing_bathrooms = {"error": "missingBathrooms",
                     "status": missing_invalid_parameter}

missing_longitude = {"error": "missingLongitude",
                     "status": missing_invalid_parameter}

missing_latitude = {"error": "missingLatitude",
                    "status": missing_invalid_parameter}

missing_description = {"error": "missingDescription",
                       "status": missing_invalid_parameter}

missing_image = {"error": "missingImage",
                 "status": missing_invalid_parameter}

missing_image_index = {"error": "missingImageIndex",
                       "status": missing_invalid_parameter}

missing_senderId = {"error": "missingSenderId",
                    "status": missing_invalid_parameter}

missing_receiverId = {"error": "missingReceiverId",
                      "status": missing_invalid_parameter}

missing_message = {"error": "missingMessage",
                   "status": missing_invalid_parameter}

un_auth_listing = {"error": "unAuthListing",
                   "status": unauthorized_access}

password_mismatch = {"error": "passwordMismatch",
                     "status": unauthorized_access}

invalid_xor_condition = {"error": "missingXorCondition",
                         "status": missing_invalid_parameter}

invalid_values_required = {"error": "invalidValuesRequired",
                           "status": missing_invalid_parameter}

unallowed_message_send = {"error": "unallowedMessageSend",
                          "status": processing_failed}

invalid_message_id = {"error": "invalidMessageId",
                      "status": missing_invalid_parameter}

missing_message_id = {"error": "missingMessageId",
                      "status": missing_invalid_parameter}

missing_read_del = {"error": "missingReadDel",
                   "status": missing_invalid_parameter}

invalid_read_del = {"error": "invalidReadDel",
                   "status": missing_invalid_parameter}

missing_fb_id = {"error": "missingFbId",
                 "status": missing_invalid_parameter}

invalid_fb_id = {"error": "invalidFbId",
                 "status": missing_invalid_parameter}

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
    "squarefeet": invalid_squarefeet,
    "isPublished": invalid_published,
    "thumbnailImageIndex": invalid_thumbnail_image_index,
    "liked": invalid_liked,
    "filter": invalid_filter_bound,
    "valuesRequired": invalid_values_required,
    'images': invalid_images,
    "longitude": invalid_longitude,
    "latitude": invalid_latitude,
    "senderId": invalid_user_id,
    "phone": invalid_phone,
    "messageId": invalid_message_id,
    "readDel": missing_read_del,
    "fbId": missing_fb_id
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
    "squarefeet": missing_squarefeet,
    "isPublished": missing_published,
    "thumbnailImageIndex": missing_image_index,
    "images": missing_image,
    "description": missing_description,
    "address": missing_address,
    "liked": missing_liked,
    "longitude": missing_longitude,
    "latitude": missing_latitude,
    "senderId": missing_senderId,
    "message": missing_message,
    "phone": missing_phone_number,
    "readDel": missing_read_del,
    "messageId": missing_message_id,
    "fbId": invalid_fb_id,
    "receiverId": missing_receiverId
}
