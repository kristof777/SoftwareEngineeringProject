let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html'
})
export class MyListingsPage {

    constructor(public navCtrl: NavController) {

    }

}
