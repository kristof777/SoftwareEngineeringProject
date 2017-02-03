import {User} from "../../app/models/user";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-settings',
    templateUrl: 'settings.html'
})
export class SettingsPage {
    currentUser: User
    constructor(public navCtrl: NavController,
                private _logger: Logger) {
        //TODO: Remove fake user account
        this.currentUser = new User(null, 'test@gmail.com', 'Test', 'Test', '3062325323', null, null, null);
    }

    saveChanges() {
        this._logger.debug("Save button was clicked.");
    }

    signOut(){
        this._logger.debug("Sign-out was clicked.");
    }

}
