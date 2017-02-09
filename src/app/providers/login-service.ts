import { Injectable } from '@angular/core';
import {Http, ResponseContentType} from '@angular/http';
import 'rxjs/add/operator/map';
let assert = require('assert-plus');

@Injectable()
export class LoginService {
    data: any;

    constructor(public http: Http) {
        this.data = null;
    }

    login(email: string, password: string): void{
        /*
         * POST
         * this.http.post(URL, data, ResponseContentType.Json).subscribe(...)
         *
         * GET
         * this.http.get(URL, ResponseContentType.Json).subscribe(...)
         *
         * Ours might look something like this?
         *
         * this.http.post("https://kasperhomeapp.com/api/login/",
         *     { email: email, password: password }, ResponseContentType.Json)
         *     .subscribe(data => {
         *         this.data = data;
         *     });
         */
    }


    /** Checks a password for validity.
     *
     * @param password  the password to check
     * @precond         the password is not null
     * @returns an object with the following attributes
     *          strength    the strength of the password [0 to 4]
     *          message     a message depicting how to raise the strength
     */
    checkPass(password: string): any{
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
        }
        if(!upperCase.test(password)){
            return {
                strength: 1,
                message: "Password must include at least one upper case letter"
            };
        }
        if(!numeric.test(password)){
            return {
                strength: 2,
                message: "Password must include at least one number"
            };
        }
        if(!length.test(password)){
            return {
                strength: 3,
                message: "Password must include at least 7 characters long"
            };
        }
        return {
            strength: 4
        };
    }

}
