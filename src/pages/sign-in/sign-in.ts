let assert = require('assert-plus');
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";

import {NavController, ToastController} from 'ionic-angular';

import {SignUpPage} from '../sign-up/sign-up';
import {MainPage} from "../main/main";

@Component({
    selector: 'page-sign-in',
    templateUrl: 'sign-in.html'
})
export class SignInPage {
    email: string;
    password: string;

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                private _logger: Logger) {
    }

    pushRegister(){
        this._logger.debug("Register was clicked.");
        this.navCtrl.push(SignUpPage);
    }

    doSignIn(){
        this._logger.debug("Sign In was clicked.")

        if(this.email == "test")
            this.navCtrl.setRoot(MainPage);
        else
            this.toastCtrl.create({
                message: 'To continue, set e-mail to "test"',
                duration: 3000,
                position: 'top'
            }).present();
    }
}
