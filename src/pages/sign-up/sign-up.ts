import {Component, ViewChild} from '@angular/core';
import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');

import {NavController, ToastController, Slides} from 'ionic-angular';
import {KasperService} from '../../app/providers/kasper-service'
import {MainPage} from "../main/main";

@Component({
    selector: 'page-sign-up',
    templateUrl: 'sign-up.html',
    providers: [KasperService]
})
export class SignUpPage {
    @ViewChild(Slides) slides: Slides;
    email: string = "test@mail.com";
    password: string = "Password1";
    confirmPassword: string = "Password1";

    firstName: string = "aa";
    lastName: string ="aa";
    phoneNumber: string ="1234567890";

    province: string = "SK";
    city: string = "Saskatoon";

    selectedMode: number;

    constructor(public navCtrl: NavController,
                private _logger: Logger,
                public toastCtrl: ToastController,
                public userService: KasperService) {
    }

    doRegister(): void{
        this.userService.signUp(this.email,this.password, this.confirmPassword,this.firstName,
            this.lastName, this.phoneNumber, "", this.city, this.province, this.registerCallback);
        this.navCtrl.setRoot(MainPage);
    }

    registerCallback(data: JSON){

    }

    /**
     * Go to the next step if the fields are valid
     */
    nextStep(): void{
        if(this.confirmStep()){
            this.slides.slideTo(this.slides.getActiveIndex() + 1);
        } else {
            this._logger.error("Confirm step was false");
        }
    }

    previousStep(): void{
        if(this.slides.getActiveIndex() != 0)
            this.slides.slideTo(this.slides.getActiveIndex() - 1);
    }

    /**
     * Confirm the validity of the current step
     *
     * @returns {boolean}   true if the fields are valid
     *                      false otherwise
     */
    confirmStep(): boolean{
        this._logger.error(this.slides.getActiveIndex());
        switch(this.slides.getActiveIndex()){
            case 0:
                return this.confirmStepOne();
            case 1:
                return this.confirmStepTwo();
            case 2:
                return this.confirmStepThree();
        }
    }

    /**
     * Confirm the validity of step one
     *
     * @returns {boolean}   true if the fields are valid
     *                      false otherwise
     */
    confirmStepOne(): boolean{
        let checkPw: any = this.userService.checkPass(this.password);
        let error: string = null;

        if(!this.email || !this.password || !this.confirmPassword) {
            error = "Please fill in all required fields.";
        } else if(!this.checkEmail(this.email)) {
            error = "Please enter a valid e-mail address";
        } else if(checkPw.strengh != 4) {
            error = checkPw.message;
        } else if (this.password != this.confirmPassword){
            error = "The passwords you provided do not match.";
        }

        if(error) {
            this.toastCtrl.create({
                message: error,
                duration: 3000,
                position: 'top'
            }).present();
        }

        return !error;
    }

    confirmStepTwo(): boolean{
        let error: string = null;

        if(!this.firstName || !this.lastName || !this.phoneNumber){
            error = "Please fill in all required fields.";
        } else if (this.phoneNumber.length != 10 || !Number(this.phoneNumber)){
            error = "Please enter a valid phone number.";
        }

        if(error) {
            this.toastCtrl.create({
                message: error,
                duration: 3000,
                position: 'top'
            }).present();
        }

        return !error;
    }

    confirmStepThree(): boolean{
        let error: string = null;

        if(!this.province || !this.city){
            error = "Please fill in all required fields.";
        }
        // TODO verify the city

        if(error) {
            this.toastCtrl.create({
                message: error,
                duration: 3000,
                position: 'top'
            }).present();
        }

        return !error;
    }

    onModeSelect (mode: number): void{
        if(mode == 0){
            document.getElementById("buyMode").removeAttribute("width-25");
            document.getElementById("buyMode").setAttribute("width-75", "true");
        } else {
            document.getElementById("buyMode").removeAttribute("width-75");
            document.getElementById("buyMode").setAttribute("width-25", "true");
        }

        this.selectedMode = mode;
    }
    /**
     * Checks the input with an e-mail regex
     *
     * @param email the email to check
     * @returns {boolean} true if it was accepted by the regex, false otherwise
     */
    checkEmail(email: string): boolean{
        if (!email)
            return false;

        let regExp = new RegExp("^(.+)@(.+){2,}\.(.+){2,}");

        return (regExp.test(email));
    }
}
