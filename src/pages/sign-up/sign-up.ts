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
        this._logger.debug("Register was clicked.")
        var message = null
        var passwordStrength = null
        if (this.email == null || !(this.checkEmail(this.email))) {
            message = "Please enter a valid E-mail address"
        } else if (this.password == null){
            message = "Please enter a password"
        }
        else {
            passwordStrength = this.checkPass(this.password)
        }

        if (passwordStrength != null && passwordStrength < 4) {

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


        if (message != null) {
            this.toastCtrl.create({
                message: message,
                duration: 3000,
                position: 'top'
            }).present();
        }
        else{
            //TODO Sign in stuff
            this.navCtrl.setRoot(MainPage);
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
        if (email == null){
            return false
        }
        var regExp = new RegExp("/\S+@\S+\.\S+/")
        return (regExp.test(email))
    }


}
