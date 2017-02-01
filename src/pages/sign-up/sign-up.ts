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

    doRegister(){
        this._logger.debug("Sign Up was clicked.")

        var passwordStrength = this.checkPass(this.password)
        if(!this.checkEmail(this.email)){
            this.toastCtrl.create({
                message: 'Invalid Email address',
                duration: 3000,
                position: 'top'
            }).present();
        }else if(passwordStrength < 4){
            //add messages for each case

        }
        else if(!this.confirmTwo(this.email, this.confirmEmail)){
            this.toastCtrl.create({
                message: 'To continue, set e-mail to "test"',
                duration: 3000,
                position: 'top'
            }).present();
        }
        else {
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
        assert (email != null)
        var regExp = new RegExp("^[a-zA-Z0–9_.+-]+@[a-zA-Z0–9-]+.[a-zA-Z0–9-.]+$")
        return regExp.test(email)
    }


}
