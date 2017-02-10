import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import {Listing} from "../models/listing";
import {Location} from "../models/location";
import {Logger} from "angular2-logger/core";

@Injectable()
export class SavedListingProvider {
    myListings: any;
    favListings: any;

    constructor(public http: Http,
                private _logger: Logger) {

        this.favListings = [
            new Listing(1, 1, new Location("SK", "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0), 3, 4, 1800, 288000, "Curabitur nec lacus diam. Maecenas placerat metus egestas sollicitudin malesuada. Mauris semper vehicula metus. Quisque faucibus nisl nec eros mollis, sit amet vulputate metus vehicula. Suspendisse non suscipit lorem. Ut metus magna, sollicitudin vitae facilisis vel, facilisis vel tellus. Donec bibendum pretium mauris. Praesent facilisis risus ut est accumsan imperdiet.", false, "2017-01-01","2017-01-20", "http://placehold.it/50x50", ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081","http://placehold.it/1920x1082","http://placehold.it/1920x1082","http://placehold.it/1920x1082"]),
            new Listing(2, 1, new Location("SK", "Regina", "1234 Regina St.", "C3B2A1", 0.0, 0.0), 2, 2, 1400, 248000, "Cras vel porttitor orci. Sed eget efficitur sapien, in commodo felis. Etiam ac erat tincidunt, pellentesque ante ut, convallis purus. In ullamcorper mi at fermentum interdum. Proin id orci enim. Sed pharetra turpis ligula, non lacinia ipsum aliquet lacinia. Sed urna risus, pharetra in dui ut, vulputate tincidunt dui.", false, "2017-01-08", "2017-01-17", "http://placehold.it/50x50", ["http://placehold.it/1280x720", "http://placehold.it/1280x721","http://placehold.it/1280x720"])
        ];

        this.myListings = [
            new Listing(1, 1, new Location("SK", "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0), 3, 4, 1800, 288000, "yoyooyo  see i am changing metus. Quisque faucibus nisl nec eros mollis, sit amet vulputate metus vehicula. Suspendisse non suscipit lorem. Ut metus magna, sollicitudin vitae facilisis vel, facilisis vel tellus. Donec bibendum pretium mauris. Praesent facilisis risus ut est accumsan imperdiet.", false, "2017-01-01","2017-01-20", "http://placehold.it/50x50", ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081","http://placehold.it/1920x1082","http://placehold.it/1920x1082","http://placehold.it/1920x1082"]),
            new Listing(2, 1, new Location("SK", "Regina", "1234 Regina St.", "C3B2A1", 0.0, 0.0), 2, 2, 1400, 248000, "This changed from random text efficitur sapien, in commodo felis. Etiam ac erat tincidunt, pellentesque ante ut, convallis purus. In ullamcorper mi at fermentum interdum. Proin id orci enim. Sed pharetra turpis ligula, non lacinia ipsum aliquet lacinia. Sed urna risus, pharetra in dui ut, vulputate tincidunt dui.", false, "2017-01-08", "2017-01-17", "http://placehold.it/50x50", ["http://placehold.it/1280x720", "http://placehold.it/1280x721","http://placehold.it/1280x720"])
        ];
    }

    /**
     * Add a listing to the local database
     */
    addListing(){
        this._logger.error("ListingProvider.addListing is not implemented.");
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
