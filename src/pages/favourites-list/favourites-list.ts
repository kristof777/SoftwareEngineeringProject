let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-favourites-list',
    templateUrl: 'favourites-list.html'
})
export class FavouritesListPage {

    constructor(public navCtrl: NavController) {

    }

}
