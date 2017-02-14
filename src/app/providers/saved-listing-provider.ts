import { Injectable } from '@angular/core';
import { SQLite } from 'ionic-native';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import {Listing} from "../models/listing";
import {Logger} from "angular2-logger/core";

@Injectable()
export class SavedListingProvider {
    myListings: any;
    favListings: any;

    constructor(public http: Http,
                private _logger: Logger) {

        this.loadListings();
        this.updateListings();
    }

    /**
     * Load listings saved on the device
     */
    loadListings(): void{


        this.updateListings();
    }

    /**
     * Update the listings on the device with the ones from the server if they are outdated.
     *
     * Note: If this causes performance issues, we can move it to only be called when they open the detail page
     */
    updateListings(): void{
        // TODO get the users listings and favourites from the server
        // If they already have listings on their device, we must check if the modifiedDate of the listing on the
        // server is newer than the listing on the device and react accordingly (update information etc.)
    }

    /**
     * Add a listing to the users favourites
     *
     * @param listing   the listing the user favourited
     */
    addFavourite(listing: Listing): void{
        let key: string = listing.listingId.toString();
        this.favListings[key] = listing;
    }

    /**
     * Add a listing to the local database
     *
     * @param listing   the listing the user created
     */
    addListing(listing: Listing): void{
        let key: string = listing.listingId.toString();
        this.myListings[key] = listing;
    }

    /**
     * Remove a listing from the users's favourites
     *
     * @param listingId  the id of the listing to remove
     */
    removeFavourite(listingId: number): void{
        let key: string = listingId.toString();
        delete this.favListings[key];
    }

    /**
     * Remove a listing from the device
     *
     * @param listingId the id of the listing to remove
     */
    removeListing(listingId: number): void{
        let key: string = listingId.toString();
        delete this.myListings[key];
    }
}
