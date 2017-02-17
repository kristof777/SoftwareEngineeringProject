import { Injectable } from '@angular/core';
import {Http, ResponseContentType} from '@angular/http';
import {KasperConfig} from "../kasper-config";
import 'rxjs/add/operator/map';
import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');

@Injectable()
export class UserService {

    constructor(public http: Http,
                private _logger: Logger) {
    }

    /**
     * Send a login request to the server
     *
     * @param email     the email to sign in with
     * @param password  the password to sign in with
     * @param cbLogin   the callback for the data
     */
    login(email: string, password: string, cbLogin: (data: any) => void): void{
        let body = new FormData();
        body.append('email', email);
        body.append('password', password);

        this.http.post(KasperConfig.API_URL + "/signin", body, ResponseContentType.Json)
            .subscribe(data => {
                cbLogin(data);
            }, error => {
                this._logger.log("Oooops, sign in failed!");
                this._logger.log(error);
            });
    }

    /**
     * Send a request to register the user in the database, then log them in
     *
     * @param email             the email of the user
     * @param password          the desired password
     * @param confirmedPassword the password confirmation
     * @param firstName         the first name of the user
     * @param lastName          the last name of the user
     * @param phoneNumber       the primary phone number of the user
     * @param city              the city of the user
     */
    signUp(email: string, password: string, confirmedPassword: string, firstName: string,
           lastName: string, phoneNumber: string, city: string): void{
        let body = new FormData();
        body.append('email', email);
        body.append('password', password);
        body.append('confirmedPassword', confirmedPassword);
        body.append('firstName', firstName);
        body.append('lastName', lastName);
        body.append('phone1', phoneNumber);
        body.append('city', city);
        body.append('province', "SK");
        body.append('postalcode', "123456");

        this.http.post(KasperConfig.API_URL + "/createuser", body, ResponseContentType.Json)
            .subscribe(data => {
                this._logger.log(data);
                // TODO use the response to login
            }, error => {
                this._logger.log("Oooops, sign in failed!");
                this._logger.log(error);
            });
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
        assert (password != null);
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
