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
    myListings: Listing[];
    favListings: Listing[];

    listModel : string;
    constructor(public navCtrl: NavController,
                public savedListings: SavedListingProvider,
                private _logger: Logger) {
        this.myListings = savedListings.myListings;
        this.favListings = savedListings.favListings;

        this.listModel="listings"
    }

    /**
     *
     * @param listing listing clicked by user
     * Shows up the information about listing, in browse mode
     */
    clickFavListing(listing:Listing){
        // open about that listing
        this.navCtrl.push(BrowsePage,{
            data:this.favListings,
            cursor:this.favListings.indexOf(listing)
        });
        this._logger.debug("Listing  " + listing +" was clicked");
    }

    /**
     *
     * @param listing listing clicked by user
     * Shows up the information about listing, in browse mode
     */
    clickMyListing(listing:Listing){
            this.navCtrl.push(BrowsePage, {
                data: this.myListings,
                cursor: this.myListings.indexOf(listing)
            });
            this._logger.debug("Listing  " + listing + " was clicked")

    }

    /**
     *
     * @param listing: listing to be edited
     */
    deleteFavListing(listing:Listing) {
        this.favListings.splice(this.favListings.indexOf(listing),1);
    }

    /**
     *
     * @param listing: listing to be edited
     */
    editMyListing(listing:Listing){
        this.navCtrl.push(EditListingsPage,{
            data:listing
        });
        this._logger.debug("Trying to edit...")

    }

    /**
     *
     * @param listing: listing to be deleted
     */
    deleteMyListing(listing:Listing){
        this.myListings.splice(this.myListings.indexOf(listing),1);
    }

    /**
     *  Takes you to listing page
     */
    addListing(){
        this.navCtrl.push(AddListingPage);
    }

    /**
     * called when segment is changed to Listings
     */
    selectListings(){
        this._logger.debug("Listing menu selected");
    }

    /**
     * called when segment is changed to Favourites
     */
    selectFavourites(){
        this._logger.debug("Favourites menu selected");
    }



}
