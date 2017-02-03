import { Component } from '@angular/core';
import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');

import {NavController, ToastController} from 'ionic-angular';
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

    /**Function which is called when the user clicks the register button.
     * This will check the fields and either complain or accept the registration.
     */
    doRegister() {
        this._logger.debug("Register was clicked.");
        var message = null;
        var passwordStrength = null;

        if (!this.email || !(this.checkEmail(this.email))) {
            message = "Please enter a valid E-mail address";
        } else if (!this.confirmTwo(this.email, this.confirmEmail)) {
            message = "E-mails do not match";
        } else if (!this.password){
            message = "Please enter a password";
        } else {
            passwordStrength = this.checkPass(this.password);

            if (passwordStrength != null && passwordStrength < 4) {
                if (passwordStrength == 0) {
                    message = "Password must include at least one lower case letter";
                } else if (passwordStrength == 1) {
                    message = "Password must include at least one upper case letter";
                } else if (passwordStrength == 2) {
                    message = "Password must include at least one number";
                } else if (passwordStrength == 3) {
                    message = "Password must be longer than 7 characters";
                }
            } else if (!this.confirmTwo(this.password, this.confirmPassword)) {
                message = "Passwords do not match";
            } else if (!this.firstName){
                message = "Please enter your first name";
            } else if (!this.lastName){
                message = "Please enter your last name";
            } else if (!this.phoneNumber){
                message = "Please enter your phone-number";
            } else if (!this.city){
                message = "Please enter the name of your city";
            }
        }

        if (message) {
            this.toastCtrl.create({
                message: message,
                duration: 3000,
                position: 'top'
            }).present();
        } else {
            //TODO Sign in stuff
            this.navCtrl.setRoot(MainPage);
        }
    }


    /** Checks a password for validity.
     *
     * @param password String password
     * @precond passwrd is not null
     * @returns {number} which represents the password strength: 0 if success, 1 if no lower case letter,
     * 2 if no upper case, 3 if no numeric, 4 if the password is below 7 characters.
     */
    checkPass(password: string){
        assert (password != null);
        var lowerCase = new RegExp("^(?=.*[a-z])");
        var upperCase = new RegExp("^(?=.*[A-Z])");
        var numeric = new RegExp("^(?=.*[0-9])");
        var length = new RegExp("^(?=.{7,})");

        if(!lowerCase.test(password)){
            return 0;
        }
        if(!upperCase.test(password)){
            return 1;
        }
        if(!numeric.test(password)){
            return 2;
        }
        if(!length.test(password)){
            return 3;
        }
        return 4;
    }

    /**Checks if two parameters are equal.
     *
     * @param firstField first string to compare
     * @param secondField second string to compare
     * @returns {boolean} true if they match, false otherwise.
     */
    confirmTwo(firstField: string, secondField: string){
        return (firstField == secondField)
    }

    /**Checks the input with an e-mail regex
     *
     * @param email the email to check
     * @returns {boolean} true if it was accepted by the regex, false otherwise
     */
    checkEmail(email: string){
        if (!email){
            return false
        }
        var regExp = new RegExp("^(.+)@(.+){2,}\.(.+){2,}")
        return (regExp.test(email))
    }


}
