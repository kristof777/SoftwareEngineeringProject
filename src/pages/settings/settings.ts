import {User} from "../../app/models/user";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";
import {Location} from "../../app/models/location";
import {Province} from "../../app/models/province";

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-settings',
    templateUrl: 'settings.html'
})
export class SettingsPage {
    private provinces: Province[];
    currentUser: User;

    constructor(public navCtrl: NavController,
                private _logger: Logger) {
        this.provinces = Province.asArray;
        //TODO: Remove fake user account
        let userID: number = 1;
        let email: string = "john.doe@gmail.com";
        let firstName: string = "John";
        let lastName: string = "Doe";
        let phoneNumber: string = "3065555555";
        let location: Location = new Location(Province.SK, "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0);

        this.currentUser = new User(userID, email, firstName, lastName, phoneNumber, null, null, location);
    }

    saveChanges() {
        this._logger.debug("Save button was clicked.");
    }

    signOut(){
        this._logger.debug("Sign-out was clicked.");
    }

}
