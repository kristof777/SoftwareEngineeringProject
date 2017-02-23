import { Injectable } from '@angular/core';
import {Http, ResponseContentType} from '@angular/http';
import {KasperConfig} from "../kasper-config";
import 'rxjs/add/operator/map';
import {Logger} from "angular2-logger/core";
import {Filter} from "../models/filter";
import {Listing} from "../models/listing";
import {LoginService} from "./login-service";
let assert = require('assert-plus');

@Injectable()
export class KasperService {

    constructor(public http: Http,
                public loginService: LoginService,
                private _logger: Logger) {
    }

    getUserId(): number{
        return this.loginService.getUserId();
    }

    getToken(): string{
        return this.loginService.getToken();
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
     * @param cbLogin   the callback for the data
     */
    login(email: string, password: string, cbLogin: (data: JSON) => void): void{
        let body = new FormData();
        body.append('email', email);
        body.append('password', password);

        this.http.post(KasperConfig.API_URL + "/signIn", body, ResponseContentType.Json)
            .subscribe(data => {
                cbLogin(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    /**
     * Send a login request to the server using a token
     *
     * The return data is as follows
     * {
     *      token: string
     * }
     *
     * @param cbLogin   the callback for the data
     */
    loginWithToken(cbLogin: (data: JSON) => void): void{
        let body = new FormData();
        this.appendAuthentication(body);

        this.http.post(KasperConfig.API_URL + "/signInToken", body, ResponseContentType.Json)
            .subscribe(data => {
                cbLogin(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    // TODO
    confirmEmail(): void{}

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
     * @param cbSignUp          the callback for the data
     */
    signUp(email: string, password: string, confirmedPassword: string, firstName: string,
            lastName: string, phone1: string, phone2: string, city: string, province: string,
            cbSignUp: (data: JSON) => void): void{
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

        this.http.post(KasperConfig.API_URL + "/createUser", body, ResponseContentType.Json)
            .subscribe(data => {
                cbSignUp(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    /**
     * Send a request to update the user's profile
     *
     * @param changeValues  a dictionary of values to change, valid keys are as follows
     *                      firstName, lastName, phone1, phone2, city, province, email
     * @param cbEditAccount the callback for the data
     */
    editUser(changeValues: JSON, cbEditAccount: (data: JSON) => void): void {
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('changeValues', changeValues);

        this.http.post(KasperConfig.API_URL + "/editUser", body, ResponseContentType.Json)
            .subscribe(data => {
                cbEditAccount(data.json());
            }, error => {
                this._logger.log(error);
            });
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
     * @param cbChangePassword      the callback for the data
     */
    changePassword(oldPassword: string, newPassword: string, newPasswordConfirmed: string,
                   cbChangePassword: (data: JSON) => void): void{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('oldPassword', oldPassword);
        body.append('newPassword', newPassword);
        body.append('newPasswordConfirmed', newPasswordConfirmed);

        this.http.post(KasperConfig.API_URL + "/changePassword", body, ResponseContentType.Json)
            .subscribe(data => {
                cbChangePassword(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    /**
     * Request the favourite listings of a user
     *
     * The return data is as follows
     * {
     *      listings: Listing[]
     * }
     *
     * @param cbGetFavourites   the callback for the data
     */
    getFavourites(cbGetFavourites: (data: JSON) => void): void{
        let body = new FormData();
        this.appendAuthentication(body);

        this.http.post(KasperConfig.API_URL + "/favouritesListingUser", body, ResponseContentType.Json)
            .subscribe(data => {
                cbGetFavourites(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    /**
     * Submit a request to like/dislike a listing
     *
     * @param listingId             the listing id
     * @param liked                 do they like it
     * @param cbLikeDislikeListing  the callback for the data
     */
    likeDislikeListing(listingId: number, liked: boolean, cbLikeDislikeListing: (data: JSON) => void): void{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);
        body.append('liked', liked);

        this.http.post(KasperConfig.API_URL + "/likeDislikeListing", body, ResponseContentType.Json)
            .subscribe(data => {
                cbLikeDislikeListing(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    /**
     * Submit a request to get listings according to the specified filter
     *
     * The return data is as follows
     * {
     *      listings: Listing[]
     * }
     *
     * @param cursor            the index of the last loaded listing
     * @param lastListingId     the last listing ID received
     * @param filter            the filter to apply
     * @param cbGetListing      the callback for the data
     */
    getListings(cursor: number, lastListingId: number, filter: Filter, cbGetListing:
                (data: JSON) => void): void{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('cursor', cursor);
        body.append('lastListingId', lastListingId);
        body.append('filter', JSON.stringify(filter));

        this.http.post(KasperConfig.API_URL + "/getListings", body, ResponseContentType.Json)
            .subscribe(data => {
                cbGetListing(data.json());
            }, error => {
                this._logger.log(error);
            });
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
     * @param cbCreateListing   the callback for the data
     */
    createListings(listing: Listing, cbCreateListing: (data: JSON) => void): void{
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

        this.http.post(KasperConfig.API_URL + "/createListing", body, ResponseContentType.Json)
            .subscribe(data => {
                cbCreateListing(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    /**
     * Send a request to update a listing
     *
     * @param changeValues  a dictionary of values to change, valid keys are as follows
     *                      province, city, address, price, sqft, bedrooms, bathrooms,
     *                      description, images, thumbnailImageIndex, isPublished
     * @param cbEditAccount the callback for the data
     */
    editListing(changeValues: JSON, cbEditAccount: (data: JSON) => void): void {
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('changeValues', changeValues);

        this.http.post(KasperConfig.API_URL + "/editListing", body, ResponseContentType.Json)
            .subscribe(data => {
                cbEditAccount(data.json());
            }, error => {
                this._logger.log(error);
            });
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
     * @param cbRequestContactInfo  the callback for the data
     */
    requestContactInformation(listingId: number, cbRequestContactInfo: (data: JSON) => void): void{
        let body = new FormData();
        this.appendAuthentication(body);
        body.append('listingId', listingId);

        this.http.post(KasperConfig.API_URL + "/requestContactInformation", body
            , ResponseContentType.Json)
            .subscribe(data => {
                cbRequestContactInfo(data.json());
            }, error => {
                this._logger.log(error);
            });
    }

    /**
     * Appends required information for all calls
     */
    appendAuthentication(body: FormData){
        body.append('userId', this.getUserId());
        body.append('token', this.getToken);
    }

     /** Checks a password for validity.
     *
     * @param password  the password to check
     * @precond         the password is not null
     * @returns {strength, message}
     *          strength    the strength of the password [0 to 4]
     *          message     a message depicting how to raise the strength
     */
    checkPass(password: string): Object{
        let lowerCase = new RegExp("^(?=.*[a-z])");
        let upperCase = new RegExp("^(?=.*[A-Z])");
        let numeric = new RegExp("^(?=.*[0-9])");
        let length = new RegExp("^(?=.{7,})");

        if(!lowerCase.test(password)){
            return {
                strength: 0,
                message: "Password must include at least one lower case letter"
            };
        } else if(!upperCase.test(password)){
            return {
                strength: 1,
                message: "Password must include at least one upper case letter"
            };
        } else if(!numeric.test(password)){
            return {
                strength: 2,
                message: "Password must include at least one number"
            };
        } else if(!length.test(password)){
            return {
                strength: 3,
                message: "Password must include at least 7 characters long"
            };
        } else {
            return {
                strength: 4
            };
        }
    }
}
