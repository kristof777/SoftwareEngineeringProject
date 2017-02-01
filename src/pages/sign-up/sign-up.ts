import { Component } from '@angular/core';
import {Logger} from "angular2-logger/core";

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
        this._logger.debug("Sign In was clicked.")

        if(!this.confirmTwo(this.email, this.confirmEmail)){
            this.toastCtrl.create({
                message: 'To continue, set e-mail to "test"',
                duration: 3000,
                position: 'top'
            }).present();
        }else {
            this.navCtrl.setRoot(MainPage);
        }

    }

    checkPass(password: string){


    }

    confirmTwo(firstField: string, secondField: string){
        return (firstField == secondField)
    }

    checkEmail(email: string){

    }


}
