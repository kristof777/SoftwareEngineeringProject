let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Location} from "./location";
import {SavedListingProvider} from "../../app/providers/saved-listings-provider";
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";



@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html',
    providers: [SavedListingProvider]
})
export class MyListingsPage {

    storedData: Listing[];

    constructor(public navCtrl: NavController, public sListings: SavedListingProvider, private _logger: Logger) {
        this.storedData = sListings.data;
    }

    haveFun(listingId:number){
        // open about that listing
        this._logger.debug("Listing Id " + listingId +" was clicked");
    }

}
