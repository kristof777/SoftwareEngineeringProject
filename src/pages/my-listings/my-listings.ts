let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Location} from "./location";
import {SavedListingProvider} from "../../app/providers/saved-listing-provider";
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";
import {BrowsePage} from "../browse/browse"
import {EditListingsPage} from "../edit-listings/edit-listings"
import {AddListingPage} from "../add-listing/add-listing"

@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html',
    providers: [SavedListingProvider]

})
export class MyListingsPage {
    listings: Listing[];

    listModel : string;
    constructor(public navCtrl: NavController,
                public savedListings: SavedListingProvider,
                private _logger: Logger) {
        this.listings = savedListings.myListings;

        this.listModel="listings"
    }

    /**
     * Shows up the information about listing, in browse mode
     *
     * @param listing listing clicked by user
     */
    selectListing(listing:Listing){
            this.navCtrl.push(BrowsePage, {
                data: this.listings,
                cursor: this.listings.indexOf(listing)
            });
            this._logger.debug("Listing  " + listing + " was clicked")
    }

    /**
     *
     * @param listing: listing to be edited
     */
    editListing(listing:Listing){
        this.navCtrl.push(EditListingsPage,{
            data:listing
        });
        this._logger.debug("Trying to edit...")

    }

    /**
     *
     * @param listing: listing to be deleted
     */
    deleteListing(listing:Listing){
        let selectedIndex = this.listings.indexOf(listing);
        this.listings.splice(selectedIndex, 1);
    }

    /**
     *  Takes you to listing page
     */
    addListing(){
        this.navCtrl.push(AddListingPage);
    }
}
