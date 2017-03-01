import {ListingProvider} from "../../app/providers/listing-provider";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";
import {DetailPage} from "../detail/detail"
import {LoginService} from "../../app/providers/login-service";

@Component({
    selector: 'page-favourites',
    templateUrl: 'favourites.html',
    providers: [ListingProvider]

})
export class FavouritesPage {
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public listingProvider: ListingProvider,
                public loginService: LoginService,
                private _logger: Logger) {

        this.listings = Array();
        // let data = listingProvider.savedListings.favListings;
        // this.listings = Object.keys(data).map(key => data[key]);
    }

    /**
     * Shows up the information about listing, in browse mode
     *
     * @param listing listing clicked by user
     */
    selectListing(listing:Listing){
        // open about that listing
        this.navCtrl.push(DetailPage,{
            data:this.listings,
            cursor:this.listings.indexOf(listing)
        });
        this._logger.debug("Listing " + this.listings.indexOf(listing) + " was clicked");
    }

    /**
     * Remove a listing from the user's favourites
     *
     * @param listing: listing to unfavourited
     */
    unfavourite(listing:Listing) {
        let selectedIndex = this.listings.indexOf(listing);
        this.listings.splice(selectedIndex, 1);
    }
}
