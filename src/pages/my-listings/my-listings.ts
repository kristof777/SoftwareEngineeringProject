let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Location} from "./location";
import {SavedListingProvider} from "../../app/providers/saved-fav-listings-provider";
import {MineListingProvider} from "../../app/providers/saved-mine-listings-provider";
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";
import {BrowsePage} from "../browse/browse.ts"
import {EditListingsPage} from "../edit-listings/edit-listings.ts"



@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html',
    providers: [SavedListingProvider,MineListingProvider]

})
export class MyListingsPage {

    mineSavedData: Listing[];
    favSavedData: Listing[];
    listModel : string;
    constructor(public navCtrl: NavController,
                public sListings: SavedListingProvider,
                public mListings: MineListingProvider,
                private _logger: Logger) {
        this.favSavedData = sListings.data;
        this.mineSavedData = mListings.data;
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
            data:this.favSavedData,
            cursor:this.favSavedData.indexOf(listing)
        });
        this._logger.debug("Listing  " + listing +" was clicked");
    }

    /**
     *
     * @param listing listing clicked by user
     * Shows up the information about listing, in browse mode
     */
    clickMineListing(listing:Listing){
        this.navCtrl.push(BrowsePage,{
            data:this.mineSavedData,
            cursor:this.mineSavedData.indexOf(listing)
        });
        this._logger.debug("Listing  " + listing +" was clicked")

    }

    /**
     *
     * @param listing: listing to be edited
     */
    deleteFavListing(listing:Listing) {
        this.favSavedData.splice(this.favSavedData.indexOf(listing),1);
    }

    /**
     *
     * @param listing: listing to be edited
     */
    editMineListing(listing:Listing){
        this.navCtrl.push(EditListingsPage,{
            data:listing
        });
        this._logger.debug("Trying to edit...")

    }

    /**
     *
     * @param listing: listing to be deleted
     */
    deleteMineListing(listing:Listing){
        this.mineSavedData.splice(this.mineSavedData.indexOf(listing),1);
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
