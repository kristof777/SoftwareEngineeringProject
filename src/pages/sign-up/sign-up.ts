import { Component } from '@angular/core';
import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');

import {NavController, ToastController} from 'ionic-angular';
import {MainPage} from "../main/main";
import {ListingProvider} from "../../app/providers/listing-provider"

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
                public toastCtrl: ToastController,
                private listingProvider: ListingProvider) {

    }

    /**Function which is called when the user clicks the register button.
     * This will check the fields and either complain or accept the registration.
     */
    doRegister(): void{
        this._logger.debug("Register was clicked.");
        let message = null;
        let passwordCheck = null;

        if (!this.email || !(this.checkEmail(this.email))) {
            message = "Please enter a valid E-mail address";
        } else if (!this.confirmTwo(this.email, this.confirmEmail)) {
            message = "E-mails do not match";
        } else if (!this.password){
            message = "Please enter a password";
        } else {
            passwordCheck = ListingProvider.checkPass(this.password);

            if (passwordCheck.strength < 4) {
                message = passwordCheck.message;
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


    /**Checks if two parameters are equal.
     *
     * @param firstField first string to compare
     * @param secondField second string to compare
     * @returns {boolean} true if they match, false otherwise.
     */
    confirmTwo(firstField: string, secondField: string): boolean{
        return (firstField == secondField);
    }

    /**Checks the input with an e-mail regex
     *
     * @param email the email to check
     * @returns {boolean} true if it was accepted by the regex, false otherwise
     */
    checkEmail(email: string): boolean{
        if (!email){
            return false;
        }
        let regExp = new RegExp("^(.+)@(.+){2,}\.(.+){2,}");
        return (regExp.test(email));
    }


}
