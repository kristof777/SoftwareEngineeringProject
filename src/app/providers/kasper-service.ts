let assert = require('assert-plus');
import {Injectable} from "@angular/core";
import {Http, ResponseContentType} from "@angular/http";
import {KasperConfig} from "../kasper-config";
import "rxjs/add/operator/map";
import {Logger} from "angular2-logger/core";
import {Filter} from "../models/filter";
import {Listing} from "../models/listing";
import {LoginService} from "./login-service";
import {FormControl} from "@angular/forms";

@Injectable()
export class KasperService {

    constructor(public http: Http,
                public loginService: LoginService,
                private _logger: Logger) {
    }

    /**
     * Send a login request to the server
     *
     * The return data is as follows
     * {
     *      token: string,
     *      userId: int,
     *      email: string,
     *      firstName: string,
     *      lastName: string,
     *      phone1: string,
     *      phone2:string,
     *      city: string,
     *      province: string
     *  }
     *
     * @param email     the email to sign in with
     * @param password  the password to sign in with
     */
    login(email: string, password: string): any{
        let body = new FormData();
        body.append('email', email);
        body.append('password', password);

        return this.http.post(KasperConfig.API_URL + "/signIn", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a login request to the server using a token
     *
     * The return data is as follows
     * {
     *      token: string
     * }
     */
    loginWithToken(): any{
        let body = new FormData();
        this.appendAuthentication(body);

        return this.http.post(KasperConfig.API_URL + "/signInToken", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    confirmEmail(): any{
        let body = new FormData();
        this.appendAuthentication(body);

        return this.http.post(KasperConfig.API_URL + "/confirmEmail", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to register the user in the database, then log them in
     *
     * The return data is as follows
     * {
     *      token: string,
      *     useId: int
     * }
     *
     * @param email             the email of the user
     * @param password          the desired password
     * @param confirmedPassword the password confirmation
     * @param firstName         the first name of the user
     * @param lastName          the last name of the user
     * @param phone1            primary phone number
     * @param phone2            secondary phone number
     * @param city              the city of the user
     * @param province          abbreviation of province
     */
    signUp(email: string, password: string, confirmedPassword: string, firstName: string,
            lastName: string, phone1: string, phone2: string, city: string, province: string): any{
        let body = new FormData();
        body.append('email', email);
        body.append('password', password);
        body.append('confirmedPassword', confirmedPassword);
        body.append('firstName', firstName);
        body.append('lastName', lastName);
        body.append('phone1', phone1);
        body.append('phone2', phone2);
        body.append('city', city);
        body.append('province', province);

        return this.http.post(KasperConfig.API_URL + "/createUser", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to update the user's profile
     *
     * @param changeValues  a dictionary of values to change, valid keys are as follows
     *                      firstName, lastName, phone1, phone2, city, province, email
     */
    editUser(changeValues: Object): any {
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('changeValues', changeValues);

        return this.http.post(KasperConfig.API_URL + "/editUser", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to change the user's password
     *
     * The return data is as follows
     * {
     *      token: string
     * }
     *
     * @param oldPassword           the current password of the user
     * @param newPassword           the new password for the user
     * @param newPasswordConfirmed  the new password for the user
     */
    changePassword(oldPassword: string, newPassword: string, newPasswordConfirmed: string): any{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('oldPassword', oldPassword);
        body.append('newPassword', newPassword);
        body.append('newPasswordConfirmed', newPasswordConfirmed);

        return this.http.post(KasperConfig.API_URL + "/changePassword", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Request the favourite listings of a user
     *
     * The return data is as follows
     * {
     *      listings: Listing[]
     * }
     */
    getFavourites(): any{
        let body = new FormData();
        this.appendAuthentication(body);

        return this.http.post(KasperConfig.API_URL + "/favouritesListingUser", body,
            ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Submit a request to like/dislike a listing
     *
     * @param listingId             the listing id
     * @param liked                 do they like it
     */
    likeDislikeListing(listingId: number, liked: boolean): any{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);
        body.append('liked', liked);

        return this.http.post(KasperConfig.API_URL + "/likeDislikeListing", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Submit a request to get listings according to the specified filter
     *
     * The return data is as follows
     * {
     *      listings: Listing[]
     * }
     *
     * @param filter            the filter to apply
     */
    getListings(filter: Filter): any{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('filter', JSON.stringify(filter));

        return this.http.post(KasperConfig.API_URL + "/getListings", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Submit a request to create a listing
     *
     * The return data is as follows
     * {
     *      listingId: number
     * }
     *
     * @param listing           the listing
     */
    createListings(listing: Listing): any{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('province', listing.location.province.abbr);
        body.append('city', listing.location.city);
        body.append('address', listing.location.address);
        body.append('price', listing.price);
        body.append('sqft', listing.squarefeet);
        body.append('bedrooms', listing.bedrooms);
        body.append('bathrooms', listing.bathrooms);
        body.append('description', listing.description);
        body.append('images', JSON.stringify(listing.images));
        body.append('thumbnailImageIndex', 0);
        body.append('isPublished', listing.isPublished);

        return this.http.post(KasperConfig.API_URL + "/createListing", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to update a listing
     *
     * @param changeValues  a dictionary of values to change, valid keys are as follows
     *                      province, city, address, price, sqft, bedrooms, bathrooms,
     *                      description, images, thumbnailImageIndex, isPublished
     */
    editListing(changeValues: JSON): any {
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('changeValues', changeValues);

        return this.http.post(KasperConfig.API_URL + "/editListing", body, ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Send a request to get the contact information for a listing
     *
     * The return data is as follows
     * {
     *       phone1: string,
     *       phone2: string,
     *       email: string
     * }
     *
     * @param listingId             the listing id
     */
    requestContactInformation(listingId: number): any{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);

        return this.http.post(KasperConfig.API_URL + "/requestContactInformation", body
            , ResponseContentType.Json)
            .map(response => response.json());
    }

    /**
     * Appends required information for all calls
     */
    appendAuthentication(body: FormData): void{
        body.append('userId', this.loginService.getUserId());
        body.append('token', this.loginService.getToken());
    }

    /**
    * Checks a password for validity.
    *
    * @param c  the form control for the check
    * @returns {strength, message}
    *          strength  the strength of the password [0 to 4]
    *          valid     whether it meets the minimum requirements
    *          message   a message depicting how to raise the strength
    */
    checkPass(c: FormControl): any{
        const requiredStrength: number = 4;

        let lowerCase = new RegExp("^(?=.*[a-z])");
        let upperCase = new RegExp("^(?=.*[A-Z])");
        let numeric = new RegExp("^(?=.*[0-9])");
        let length = new RegExp("^(?=.{7,})");

        if(!lowerCase.test(c.value)){
            return (0 == requiredStrength) ? null : {
                checkPass: {
                    strength: 0,
                    message: "Password must include at least one lower case letter"
                }
            };
        } else if(!upperCase.test(c.value)){
            return (1 == requiredStrength) ? null : {
                checkPass: {
                    strength: 1,
                    message: "Password must include at least one upper case letter"
                }
            };
        } else if(!numeric.test(c.value)){
            return (2 == requiredStrength) ? null : {
                checkPass: {
                    strength: 2,
                    message: "Password must include at least one number"
                }
            };
        } else if(!length.test(c.value)){
            return (3 == requiredStrength) ? null : {
                checkPass: {
                    strength: 3,
                    message: "Password must include at least 7 characters long"
                }
            };
        } else {
            return (4 == requiredStrength) ? null : {
                checkPass: {
                    strength: 4,
                }
            };
        }
    }

    /**
     * Check whether a phone number is valid.
     *
     * @param c the form control for the check
     * @returns null if it is valid or falsey
     *          object otherwise
     */
    checkPhone(c: FormControl): any{
        const numberRegex = new RegExp("^[0-9]{10}$");

        if(!c.value) return null;
        let input = c.value.replace(/[^0-9]*/g, "");

        if(!numberRegex.test(input)){
            return { checkPhone: { valid: false }};
        }

        return null;
    }
}
