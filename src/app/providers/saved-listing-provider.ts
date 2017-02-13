import { Injectable } from '@angular/core';
import { NativeStorage } from 'ionic-native';
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

    constructor(public http: Http,
                private _logger: Logger) {

        this.loadListings();
        this.updateListings();
    }

    /**
     * Load listings saved on the device
     */
    loadListings(): void{
        let savedFav: string;
        let savedMy: string;

        NativeStorage.getItem("favListings").then(
            data => savedFav = data,
            error => console.log(error)
        );

        NativeStorage.getItem("myListings").then(
            data => savedMy = data,
            error => console.log(error)
        );

        // If they do not have favListings or myListings, instantiate it as an empty array
        if(!savedFav){
            savedFav = JSON.stringify({
                // Add one listing under myListings by default.
                "10": new Listing(-1, -1, new Location(Province.fromAbbr("SK"), "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0), 3, 4, 1800, 288000, "Hardcoded favourite.", false, "2017-01-01", "2017-01-20", ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081", "http://placehold.it/1920x1082", "http://placehold.it/1920x1082", "http://placehold.it/1920x1082"])
            });
            NativeStorage.setItem("favListings", savedFav);
        }
        if(!savedMy){
            savedMy = JSON.stringify({
                // Add one listing under myListings by default.
                "-1": new Listing(-1, -1, new Location(Province.fromAbbr("SK"), "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0), 3, 4, 1800, 288000, "(Should be) saved to the device by default.", false, "2017-01-01", "2017-01-20", ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081", "http://placehold.it/1920x1082", "http://placehold.it/1920x1082", "http://placehold.it/1920x1082"])
            });
            NativeStorage.setItem("myListings", savedMy);
        }

        this.favListings = JSON.parse(savedFav);
        this.myListings = JSON.parse(savedMy);

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
     * Save listings to the device.
     */
    saveMyListings(): void{
        NativeStorage.setItem("myListings", JSON.stringify(this.myListings));
    }

    /**
     * Save favourites to the device.
     */
    saveFavourites(): void{
        NativeStorage.setItem("favListings", JSON.stringify(this.favListings));
    }

    /**
     * Add a listing to the users favourites
     *
     * @param listing   the listing the user favourited
     */
    addFavourite(listing: Listing): void{
        let key: string = listing.listingId.toString();
        this.favListings[key] = listing;

        this.saveFavourites();
    }

    /**
     * Add a listing to the local database
     *
     * @param listing   the listing the user created
     */
    addListing(listing: Listing): void{
        let key: string = listing.listingId.toString();
        this.myListings[key] = listing;

        this.saveMyListings();
    }

    /**
     * Remove a listing from the users's favourites
     *
     * @param listingId  the id of the listing to remove
     */
    removeFavourite(listingId: number): void{
        let key: string = listingId.toString();
        delete this.favListings[key];

        this.saveFavourites();
    }

    /**
     * Remove a listing from the device
     *
     * @param listingId the id of the listing to remove
     */
    removeListing(listingId: number): void{
        let key: string = listingId.toString();
        delete this.myListings[key];

        this.saveMyListings();
    }
}
