import { Injectable } from '@angular/core';
import { SQLite } from 'ionic-native';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import {Listing} from "../models/listing";
import {Location} from "../models/location";
import {Logger} from "angular2-logger/core";
import {Province} from "../models/province";

@Injectable()
export class SavedListingProvider {
    myListings: any;
    favListings: any;

//
//
//
// NOTE: this class has not yet been implemented
//
//
//

    constructor(public http: Http,
                private _logger: Logger) {

        this.loadListings();
        this.updateListings();
    }

    /**
     * Load listings saved on the device
     */
    loadListings(): void{
        this.myListings = [
            new Listing(0, 31, new Location(Province.PE, "City 575", "2275 Random St.", "A1B8C5", 0, 0), 7, 8, 305, 280500, "ada malesu malesu metus sollic curabitur maecenas lacus ada metus sollic nec curabitur diam egestas metus diam sollic curabitur maecenas lacus nec placerat itudin ada itudin itudin curabitur curabitur placerat maecenas maecenas malesu lacus metus sollic nec metus sollic ada maecenas placerat lacus maecenas sollic nec maecenas egestas maecenas sollic malesu diam maecenas diam diam curabitur placerat egestas ada malesu malesu ada diam itudin curabitur nec placerat egestas sollic diam sollic sollic egestas curabitur itudin sollic maecenas maecenas egestas metus egestas diam curabitur malesu diam lacus curabitur nec placerat placerat placerat diam egestas curabitur ada ada egestas maecenas nec placerat ", true, "2017-5-30", "2011-12-18", ["http://placehold.it/720x1280", "http://placehold.it/720x1280", "http://placehold.it/720x1280"]),
            new Listing(1, 22, new Location(Province.MB, "City 120", "8448 Random St.", "A2B6C9", 0, 0), 2, 8, 4840, 684000, "diam diam lacus ada egestas diam ada metus curabitur diam sollic nec diam nec malesu sollic malesu curabitur ada metus nec curabitur lacus diam placerat sollic diam metus lacus nec itudin egestas placerat malesu malesu egestas maecenas curabitur curabitur lacus malesu egestas egestas curabitur diam lacus lacus egestas metus sollic nec metus sollic placerat curabitur diam diam curabitur sollic sollic malesu itudin placerat itudin itudin malesu metus malesu maecenas egestas itudin lacus egestas diam nec curabitur nec malesu ada egestas metus ada diam placerat itudin nec curabitur ada egestas curabitur nec sollic malesu nec curabitur ada ada metus malesu ada ", true, "2010-3-3", "2010-11-1", ["http://placehold.it/720x1280", "http://placehold.it/720x1280", "http://placehold.it/720x1280"]),
            new Listing(2, 86, new Location(Province.ON, "City 534", "5556 Random St.", "A7B5C1", 0, 0), 7, 2, 1278, 317800, "diam itudin sollic curabitur placerat itudin itudin diam maecenas maecenas malesu egestas lacus placerat curabitur placerat nec ada itudin malesu egestas curabitur itudin curabitur curabitur lacus diam metus maecenas malesu curabitur metus sollic metus malesu sollic curabitur nec itudin nec curabitur diam maecenas malesu malesu nec placerat ada diam maecenas placerat placerat itudin ada metus egestas egestas egestas ada ada metus maecenas nec maecenas ada curabitur sollic maecenas lacus malesu egestas curabitur malesu malesu metus placerat ada nec diam nec placerat ada metus malesu placerat sollic maecenas sollic placerat placerat ada ada diam sollic ada maecenas lacus diam malesu malesu ", false, "2015-11-20", "2016-2-20", ["http://placehold.it/720x1280", "http://placehold.it/720x1280", "http://placehold.it/720x1280"]),
        ];
        this.favListings = {};

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
