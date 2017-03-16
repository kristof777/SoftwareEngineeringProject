import {Logger} from "angular2-logger/core";
import {Component} from "@angular/core";
import {NavParams, ViewController, AlertController} from "ionic-angular";
import {KasperService} from "../../app/providers/kasper-service";
let assert = require('assert-plus');

@Component({
    selector: 'page-change-password',
    templateUrl: 'change-password.html',
    providers: [KasperService]
})
export class ChangePasswordPage {
    currentPassword: string;
    newPassword: string;
    confirmPassword: string;

    constructor(public viewCtrl: ViewController,
                public params: NavParams,
                private alertCtrl: AlertController,
                private _logger: Logger,
                private kasperService: KasperService) {
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

        // Create the data to send back to the other page to be submitted
        let data = {
            oldPassword: this.currentPassword,
            newPassword: this.newPassword,
            confirmPassword: this.confirmPassword,
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
     *
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
