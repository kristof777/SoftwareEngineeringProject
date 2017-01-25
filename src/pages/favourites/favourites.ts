let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-favourites',
    templateUrl: 'favourites.html'
})
export class FavouritesPage {

    constructor(public navCtrl: NavController) {

    }

}
