from utils import *


def get_user(name, email, password):
    user = create_random_user()
    user["firstName"] = name
    user["email"] = email
    user["password"] = password
    user["confirmedPassword"] = password
    return user


def get_listings(bedrooms, price, bathrooms, is_published):
    listing = create_random_listing("", "")
    listing["bedrooms"] = bedrooms
    listing["price"] = price
    listing["bathrooms"] = bathrooms
    listing["isPublished"] = is_published
    return listing


users = [
    get_user("Tester 1", "test1@test.com", "123abcABC"),
    get_user("Tester 2", "test2@test.com", "123abcABC"),
    get_user("Tester 3", "test3@test.com", "123abcABC")
]

listings_published = [
    get_listings(10, 100000, 1.5, True),
    get_listings(4, 1002000, 2.5, True),
    get_listings(6, 9010000, 10, True)
]

listing_unpublished = [
    get_listings(10, 100000, 3.5, False),
    get_listings(4, 1002000, 4.5, False),
    get_listings(6, 1000, 99, False)
]
