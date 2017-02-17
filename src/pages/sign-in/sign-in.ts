let assert = require('assert-plus');
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";

import {NavController, ToastController} from 'ionic-angular';

import {SignUpPage} from '../sign-up/sign-up';
import {MainPage} from "../main/main";

import {UserService} from '../../app/providers/login-service'

@Component({
    selector: 'page-sign-in',
    templateUrl: 'sign-in.html',
    providers: [UserService]
})
export class SignInPage {
    email: string;
    password: string;

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                private _logger: Logger,
                public loginService: UserService) {
    }

    /**
     * Switch the user to the navigation screen.
     */
    pushRegister(): void{
        this._logger.debug("Register was clicked.");
        // This variable is injected through the constructor.
        this.navCtrl.push(SignUpPage);
    }

    // TODO make this function block
    /**
     * Attempt to log the user in with the provided information
     */
    doSignIn(): void{
        this._logger.debug("Sign In was clicked.");

        // "log in" if the email is set to "test"
        if(this.email == "test") {
            this.navCtrl.setRoot(MainPage);
        } else {
            this.loginService.login(this.email, this.password, this.signInCallback);
        }
    }

    /**
     * Handle data from the login request
     *
     * @param data the response from the server
     */
    signInCallback(data: any): void{
        this.navCtrl.setRoot(MainPage);
    }
}
