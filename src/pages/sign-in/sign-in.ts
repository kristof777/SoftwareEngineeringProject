let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

import {SignUpPage} from '../sign-up/sign-up';

@Component({
    selector: 'page-sign-in',
    templateUrl: 'sign-in.html'
})
export class SignInPage {

    constructor(public navCtrl: NavController) {

    }

    pushRegister(){
        console.log("Register was clicked");
        this.navCtrl.push(SignUpPage);
    }

    doSignIn(){
        console.log("Sign In was clicked");
    }
}
