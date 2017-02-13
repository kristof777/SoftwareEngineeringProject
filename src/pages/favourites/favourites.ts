import {ListingProvider} from "../../app/providers/listing-provider";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Location} from "./location";
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";
import {BrowsePage} from "../browse/browse"

@Component({
    selector: 'page-favourites',
    templateUrl: 'favourites.html',
    providers: [ListingProvider]

})
export class FavouritesPage {
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public listingProvider: ListingProvider,
                private _logger: Logger) {

        let data = listingProvider.savedListings.favListings;
        this.listings = Object.keys(data).map(key => data[key]);
    }

    /**
     * Shows up the information about listing, in browse mode
     *
     * @param listing listing clicked by user
     */
    selectListing(listing:Listing){
        // open about that listing
        this.navCtrl.push(BrowsePage,{
            data:this.listings,
            cursor:this.listings.indexOf(listing)
        });
        this._logger.debug("Listing  " + listing +" was clicked");
    }

    /**
     *
     *
     * @param listing: listing to unfavourited
     */
    unfavourite(listing:Listing) {
        let selectedIndex = this.listings.indexOf(listing);
        this.listings.splice(selectedIndex, 1);
    }
}
