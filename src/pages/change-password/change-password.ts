import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavParams, NavController, ViewController, AlertController} from 'ionic-angular';
import {UserService} from '../../app/providers/login-service'

@Component({
    selector: 'page-change-password',
    templateUrl: 'change-password.html',
    providers: [UserService]
})
export class ChangePasswordPage {
    currentPassword: string;
    newPassword: string;
    confirmPassword: string;

    constructor(public viewCtrl: ViewController,
                params: NavParams,
                private alertCtrl: AlertController,
                private _logger: Logger,
                private loginService: UserService) {
    }

    /**
     * Check whether or not the new passwords match
     * @returns {boolean} true if they match
     */
    passwordsMatch(): boolean{
        return (this.newPassword == this.confirmPassword);
    }

    /**
     * Submit the form, sending the required data back to the Settings page.
     */
    save(): void{
        // Verify the new passwords match
        if(!this.passwordsMatch()){
            this.alert("Passwords Do Not Match", "The new passwords you entered do not match.");
            return;
        }

        // Verify the new password is strong enough
        let passwordCheck: any = this.loginService.checkPass(this.newPassword);
        if(passwordCheck.strength != 4){
            this.alert("Stronger Password Required", passwordCheck.message);
            return;
        }

        // Create the data to send back to the other page to be submitted
        let data = {
            oldPassword: this.currentPassword,
            newPassword: this.newPassword,
        };

        this.viewCtrl.dismiss(data);
    }

    /**
     * Close this form without making changes
     */
    cancel(): void{
        this.viewCtrl.dismiss();
    }

    /**
     * Helper functions for quick alerts
     * @param title     the title for the alert
     * @param message   the message for the alert
     */
    alert(title: string, message: string): void{
        this.alertCtrl.create({
            title: title,
            subTitle: message,
            buttons: ["Ok"]
        }).present();
    }
}
