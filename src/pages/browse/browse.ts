let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-browse',
    templateUrl: 'browse.html'
})
export class BrowsePage {

    constructor(public navCtrl: NavController) {

    }

}
