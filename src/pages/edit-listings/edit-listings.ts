let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-edit-listings',
    templateUrl: 'edit-listings.html'
})
export class EditListingsPage {

    constructor(public navCtrl: NavController) {

    }

}
