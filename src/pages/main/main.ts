let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-main',
    templateUrl: 'main.html'
})
export class MainPage {

    constructor(public navCtrl: NavController) {

    }

    goToFavourites(){
        console.log("Favourites was clicked");
        //this.navCtrl.push(FavouritesPage);
    }

    goToFilters(){
        console.log("Filters was clicked");
        //this.navCtrl.push(FilterPage)
    }

}
