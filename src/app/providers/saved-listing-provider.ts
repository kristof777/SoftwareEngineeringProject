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

        this.updateListings();

        // These two instantiations will be handled in updateListings once it is implemented.
        this.favListings = [
            new Listing(1, 1, new Location(Province.fromAbbr("SK"), "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0), 3, 4, 1800, 288000, "Curabitur nec lacus diam. Maecenas placerat metus egestas sollicitudin malesuada. Mauris semper vehicula metus. Quisque faucibus nisl nec eros mollis, sit amet vulputate metus vehicula. Suspendisse non suscipit lorem. Ut metus magna, sollicitudin vitae facilisis vel, facilisis vel tellus. Donec bibendum pretium mauris. Praesent facilisis risus ut est accumsan imperdiet.", false, "2017-01-01","2017-01-20", ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081","http://placehold.it/1920x1082","http://placehold.it/1920x1082","http://placehold.it/1920x1082"]),
            new Listing(2, 1, new Location(Province.fromAbbr("SK"), "Regina", "1234 Regina St.", "C3B2A1", 0.0, 0.0), 2, 2, 1400, 248000, "Cras vel porttitor orci. Sed eget efficitur sapien, in commodo felis. Etiam ac erat tincidunt, pellentesque ante ut, convallis purus. In ullamcorper mi at fermentum interdum. Proin id orci enim. Sed pharetra turpis ligula, non lacinia ipsum aliquet lacinia. Sed urna risus, pharetra in dui ut, vulputate tincidunt dui.", false, "2017-01-08", "2017-01-17", ["http://placehold.it/1280x720", "http://placehold.it/1280x721","http://placehold.it/1280x720"])
        ];

        this.myListings = [
            new Listing(1, 1, new Location(Province.fromAbbr("SK"), "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0), 3, 4, 1800, 288000, "yoyooyo  see i am changing metus. Quisque faucibus nisl nec eros mollis, sit amet vulputate metus vehicula. Suspendisse non suscipit lorem. Ut metus magna, sollicitudin vitae facilisis vel, facilisis vel tellus. Donec bibendum pretium mauris. Praesent facilisis risus ut est accumsan imperdiet.", false, "2017-01-01","2017-01-20", ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081","http://placehold.it/1920x1082","http://placehold.it/1920x1082","http://placehold.it/1920x1082"]),
            new Listing(2, 1, new Location(Province.fromAbbr("SK"), "Regina", "1234 Regina St.", "C3B2A1", 0.0, 0.0), 2, 2, 1400, 248000, "This changed from random text efficitur sapien, in commodo felis. Etiam ac erat tincidunt, pellentesque ante ut, convallis purus. In ullamcorper mi at fermentum interdum. Proin id orci enim. Sed pharetra turpis ligula, non lacinia ipsum aliquet lacinia. Sed urna risus, pharetra in dui ut, vulputate tincidunt dui.", false, "2017-01-08", "2017-01-17", ["http://placehold.it/1280x720", "http://placehold.it/1280x721","http://placehold.it/1280x720"])
        ];
    }

    /**
     * Load the listings from the server
     */
    updateListings(){
        let savedFav = NativeStorage.getItem("favListings");
        let savedMy = NativeStorage.getItem("myListings");

        // If they do not have favListings or myListings, instantiate it as an empty array
        if(!savedFav){
            NativeStorage.setItem("favListings", JSON.stringify([]));
        }
        if(!savedMy){
            NativeStorage.setItem("myListings", JSON.stringify([]));
        }

        // TODO get the users listings and favourites from the server
        // If they already have listings on their device, we must check if the modifiedDate of the listing on the
        // server is newer than the listing on the device and react accordingly (update information etc.)
    }


    /**
     * Add a listing to the local database
     */
    addListing(newListing: Listing){
    }

    /**
     * Remove a listing from the database
     *
     * @param listingID the id of the listing
     */
    removeListing(listingID : number){
        this._logger.error("ListingProvider.removeListing is not implemented.");
    }

    /**
     * Search the database according to the specified filter
     *
     * @param filter the filter for the search
     *
     * @return an array of listingIDs
     */
    search(filter : any) : number[] {
        this._logger.error("ListingProvider.search is not implemented.");
        return null;
    }

    /**
     * Get the full information about a listing
     *
     * @param listingID
     * @return a listing
     */
    getListing(listingID : number) : Listing{
        this._logger.error("ListingProvider.getListing is not implemented.");
        return null;
    }

}
