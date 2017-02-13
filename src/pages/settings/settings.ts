import {User} from "../../app/models/user";
let assert = require('assert-plus');
import {ChangePasswordPage} from "../change-password/change-password";
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";
import {Location} from "../../app/models/location";
import {Province} from "../../app/models/province";

import {NavController, ModalController} from 'ionic-angular';

@Component({
    selector: 'page-settings',
    templateUrl: 'settings.html'
})
export class SettingsPage {
    private provinces: Province[];
    /** the user currently logged in to this device */
    currentUser: User;

    email: string;
    firstName: string;
    lastName: string;
    phoneNumber: string;
    province: string;
    city: string;

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                private _logger: Logger) {
        this.provinces = Province.asArray;
        //TODO: Remove fake user account
        let userID: number = 1;
        let email: string = "john.doe@gmail.com";
        let firstName: string = "John";
        let lastName: string = "Doe";
        let phoneNumber: string = "3065555555";
        let location: Location = new Location(Province.SK, "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0);

        this.currentUser = new User(userID, email, firstName, lastName, phoneNumber, null, location);
    }

    /**
     * Display the dialog for the user to update their password.
     */
    showChangePassword(): void{
        let changePasswordModal = this.modalCtrl.create(ChangePasswordPage);

        changePasswordModal.onDidDismiss(data => {
            this._logger.debug("Password change was submitted");
            // If the user saves the change
            if(data) {
                this.updatePassword(data.oldPassword, data.newPassword);
            }
        });

        changePasswordModal.present();
    }

    /**
     * Attempt to update the users password in the database.
     *
     * @param currentPassword   users input for their current password
     * @param newPassword       the new password
     */
    updatePassword(currentPassword: string, newPassword: string): void{
        // Need to verify currentPassword is correct
        // newPassword has already been checked for strength.
        this._logger.debug("Verifying and changing password");
    }

    /**
     * Update the users information according to their input
     */
    saveChanges(): void {
        this._logger.debug("Save button was clicked.");
    }

    /**
     * Sign the user out of this device.
     */
    signOut(): void{
        this._logger.debug("Sign-out was clicked.");
    }
}
