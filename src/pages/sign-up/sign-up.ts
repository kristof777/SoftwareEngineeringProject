import { Component } from '@angular/core';
import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');

import {NavController, ToastController} from 'ionic-angular';
import {SignInPage} from "../sign-in/sign-in";
import {MainPage} from "../main/main";

@Component({
    selector: 'page-sign-up',
    templateUrl: 'sign-up.html'
})
export class SignUpPage {
    email: string;
    password: string;
    confirmEmail: string;
    confirmPassword: string;
    firstName: string;
    lastName: string;
    phoneNumber: string;
    city: string;

    constructor(public navCtrl: NavController,
                private _logger: Logger,
                public toastCtrl: ToastController) {

    }

    doRegister() {
        this._logger.debug("Sign Up was clicked.")
        var message
        var passwordStrength = this.checkPass(this.password)
        assert(passwordStrength >= 0 && passwordStrength <= 4)
        if (!this.checkEmail(this.email)) {
            message = "Please enter a valid E-mail address"
        } else if (passwordStrength < 4) {

            if (passwordStrength == 0) {
                message = "must include at least one lower case letter"
            }
            else if (passwordStrength == 1) {
                message = "must include at least one upper case letter"
            }
            else if (passwordStrength == 2) {
                message = "must include at least one number"
            }
            else if (passwordStrength == 3) {
                message = "must be longer than 7 characters"
            }
        } else if (!this.confirmTwo(this.email, this.confirmEmail)) {
            message = "E-mails do not match"
        } else if (!this.confirmTwo(this.password, this.confirmPassword)) {
            message = "Passwords do not match"
        }

        else {
            this.navCtrl.setRoot(MainPage);
        }
        if (message != null) {
            this.toastCtrl.create({
                message: message,
                duration: 3000,
                position: 'top'
            }).present();
        }
    }



    //password must contain at leas one lower case, upper case, and numeric character,
    // and must be at least 7 characters long
    //:Precond string must be a valid, non null string.
    //:Returns 0 if success, 1 if no lower case letter, 2 if no upper case, 3 if no numeric, 4 if the password is below 7 characters.
    checkPass(password: string){
        assert (password != null)
        var lowerCase = new RegExp("^(?=.*[a-z])")
        var upperCase = new RegExp("^(?=.*[A-Z])")
        var numeric = new RegExp("^(?=.*[0-9])")
        var length = new RegExp("^(?=.{7,})")
        if(!lowerCase.test(password)){
            return 0
        }if(!upperCase.test(password)){
            return 1
        }if(!numeric.test(password)){
            return 2
        }if(!length.test(password)){
            return 3
        }
        return 4

    }

    confirmTwo(firstField: string, secondField: string){
        return (firstField == secondField)
    }

    checkEmail(email: string){
        assert (email != null)
        var regExp = new RegExp("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`" +
            "{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])" +
            "*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4]" +
            "[0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:" +
            "[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
        return regExp.test(email)
    }


}
