let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-add-listings',
    templateUrl: 'add-listings.html'
})
export class AddListingsPage {

    constructor(public navCtrl: NavController) {

    }

}
