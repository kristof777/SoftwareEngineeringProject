let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-add-listing',
    templateUrl: 'add-listing.html'
})
export class AddListingPage {

    constructor(public navCtrl: NavController) {

    }

}
