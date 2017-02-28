let assert = require('assert-plus');
import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from '@angular/core';
import {NavController, ModalController} from 'ionic-angular';
import {Listing} from '../../app/models/listing';
import {Logger} from "angular2-logger/core";
import {DetailPage} from "../detail/detail"
import {AddListingPage} from "../add-listing/add-listing"

@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html',
    providers: [ListingProvider]

})
export class MyListingsPage {
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                public listingProvider: ListingProvider,
                private _logger: Logger) {

        let data = listingProvider.savedListings.myListings;
        this.listings = Object.keys(data).map(key => data[key]);
    }

    /**
     * Display the detailed view for the selected listing
     *
     * @param listing listing clicked by user
     */
    selectListing(listing:Listing){
        this.navCtrl.push(DetailPage, {
            data: this.listings,
            cursor: this.listings.indexOf(listing)
        });
        this._logger.debug("Listing  " + listing + " was clicked")
    }

    /**
     * Display the edit listing view for the selected listing
     *
     * @param listing: listing to be edited
     */
    editListing(listing:Listing){
        this.navCtrl.push(AddListingPage,{
            listing:listing
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
     * Takes you to listing page
     */
    addListing(){

        this.navCtrl.push(AddListingPage);
    }

    /**
     * Get the Unpublished listing
     *
     * @returns {Listing[]}  Unpublished listing
     */
    getUnpublished(): Listing[]{
        let result: Listing[] = [];

        for(let i=0; i<this.listings.length; i++){
            if(!this.listings[i].isPublished)
                result.push(this.listings[i]);
        }

        return result;
    }

    /**
     * Get the published listing
     *
     * @returns {Listing[]}  Published listing
     */
    getPublished(): Listing[]{
        let result: Listing[] = [];

        for(let i=0; i<this.listings.length; i++){
            if(this.listings[i].isPublished)
                result.push(this.listings[i]);
        }

        return result;
    }
}
