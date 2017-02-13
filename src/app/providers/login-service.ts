import { Injectable } from '@angular/core';
import {Http, ResponseContentType} from '@angular/http';
import 'rxjs/add/operator/map';
let assert = require('assert-plus');

@Injectable()
export class UserService {
    data: any;

    constructor(public http: Http) {
        this.data = null;
    }

    login(email: string, password: string, myFunc, navCont): void{

         //POST
        // this.http.post(URL, data, ResponseContentType.Json).subscribe(...)
        //GET
        // this.http.get(URL, ResponseContentType.Json).subscribe(...)

         this.http.post("http://localhost:8080/signin",
            { email: email, password: password }, ResponseContentType.Json)
             .subscribe(data => {
                this.data = data;
                 if(data["_body"] == "Hello")
                    myFunc(navCont);
             }, error => {
                 console.log(error);
                 console.log("Oooops, sign in failed!");
             });

    }
    signUp(email:string,password:string, firstName:string,lastName:string, phoneNumber:string, city:string): void{


         this.http.post("http://localhost:8080/createuser",
            { email: email, password: password, firstName:firstName, lastName:lastName, phoneNumber:phoneNumber, city:city }, ResponseContentType.Json)
             .subscribe(data => {
                this.data = data;
                 console.log(this.data);

             }, error => {
                 console.log("error" + error);
                 console.log("Oooops, sign failed!");
             });


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
