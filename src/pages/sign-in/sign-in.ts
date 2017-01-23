let assert = require('assert-plus');
import {Component} from '@angular/core';

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
                public toastCtrl: ToastController) {
    }

    pushRegister(){
        console.log("Register was clicked.");
        this.navCtrl.push(SignUpPage);
    }

    doSignIn(){
        this.toastCtrl.create({
            message: 'To continue, set e-mail to "test"',
            duration: 3000,
            position: 'top'
        }).present();

        if(this.email == "test")
            this.navCtrl.setRoot(MainPage);
    }
}
