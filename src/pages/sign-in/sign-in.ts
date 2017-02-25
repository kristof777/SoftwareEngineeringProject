import {FormBuilder, FormGroup, Validators} from "@angular/forms";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";

import {NavController, ToastController} from 'ionic-angular';

import {SignUpPage} from '../sign-up/sign-up';
import {MainPage} from "../main/main";

import {KasperService} from '../../app/providers/kasper-service'
import {User} from "../../app/models/user";
import {Location} from "../../app/models/location";
import {Province} from "../../app/models/province";

@Component({
    selector: 'page-sign-in',
    templateUrl: 'sign-in.html',
    providers: [KasperService]
})
export class SignInPage {
    loginForm: FormGroup;
    private emailAttempted: boolean;


    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                private _logger: Logger,
                public formBuilder: FormBuilder,
                public kasperService: KasperService) {

        this.emailAttempted = false;

        this.loginForm = formBuilder.group({
            email: ['', Validators.compose([Validators.pattern("^(.+)@(.+){2,}\.(.+){2,}"), Validators.required])],
            password: ['', Validators.compose([Validators.required])],
        });
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
        if(this.loginForm.value.email == "test") {
            this.navCtrl.setRoot(MainPage);
        } else if(this.loginForm.valid){
            this.kasperService.login(this.loginForm.value.email, this.loginForm.value.password, this.signInCallback);
        } else {
            this._logger.error("Tried to submit when fields do not pass validation.");
        }
    }

    /**
     * Handle data from the login request
     *
     * @param data the response from the server
     */
    signInCallback(data: any): void{
        this.kasperService.loginService.setUser(
            new User(data.userId, data.email, data.firstName, data.lastName,  data.phone1, data.phone2,
                new Location(Province.fromAbbr(data.province), data.city, "", "", 0.0, 0.0)
        ));
        this.kasperService.loginService.setToken(data.token);

        this.navCtrl.setRoot(MainPage);
    }

    attemptEmail(){
        this.emailAttempted = true;
    }
}
