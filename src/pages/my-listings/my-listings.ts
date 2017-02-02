let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Location} from "./location";
import {SavedFavListingProvider} from "../../app/providers/saved-fav-listings-provider";
import {MineListingProvider} from "../../app/providers/saved-mine-listings-provider";
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";



@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html',
    providers: [SavedFavListingProvider,MineListingProvider]

})
export class MyListingsPage {

    storedData: Listing[];

    constructor(public navCtrl: NavController, public sListings: SavedFavListingProvider,public mListings: MineListingProvider ,private _logger: Logger) {
        this.storedData = sListings.data;
    }

    haveFun(listingId:number){
        // open about that listing
        this._logger.debug("Listing Id " + listingId +" was clicked");
    }

    selectListings(){
        this._logger.debug("Listing menu selected");
        this.storedData = this.sListings.data;
    }

    selectFavourites(){
        this._logger.debug("Favourites menu selected");
        this.storedData = this.mListings.data;
    }

}
