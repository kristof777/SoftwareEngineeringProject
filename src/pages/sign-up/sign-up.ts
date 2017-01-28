/**
 * Created by Kristof Mercier on 1/21/2017.
 */
import { Component } from '@angular/core';
import {Logger} from "angular2-logger/core";

import {NavController, ToastController} from 'ionic-angular';
import {SignInPage} from "../sign-in/sign-in";

@Component({
    selector: 'page-sign-up',
    templateUrl: 'sign-up.html'
})
export class SignUpPage {

    constructor(public navCtrl: NavController,
                private _logger: Logger,
                public toastCtrl: ToastController) {

    }

    pushSignIn(){
        this._logger.debug("Sign In was clicked.");
        this.navCtrl.push(SignInPage);
    }

}
