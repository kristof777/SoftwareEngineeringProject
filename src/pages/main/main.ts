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

    unlike(){
        console.log("Unlike was clicked");
    }

    like(){
       console.log("Like was clicked.");
    }

    nextProperty(){
        console.log("Next Property was clicked");
    }

    previousProperty(){
       console.log("Previous Property was clicked");
    }
}
