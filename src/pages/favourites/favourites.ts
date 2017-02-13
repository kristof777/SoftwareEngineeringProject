let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Location} from "./location";
import {SavedListingProvider} from "../../app/providers/saved-listing-provider";
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";
import {BrowsePage} from "../browse/browse"

@Component({
    selector: 'page-favourites',
    templateUrl: 'favourites.html',
    providers: [SavedListingProvider]

})
export class FavouritesPage {
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public savedListings: SavedListingProvider,
                private _logger: Logger) {
        this.listings = savedListings.favListings;
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
