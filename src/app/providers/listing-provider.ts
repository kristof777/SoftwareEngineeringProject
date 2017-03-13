let assert = require('assert-plus');
import "rxjs/add/operator/map";
import {Injectable} from "@angular/core";
import {Listing} from "../models/listing";
import {Logger} from "angular2-logger/core";
import {Http} from "@angular/http";
import {KasperService} from "./kasper-service";
import {Filter} from "../models/filter";

@Injectable()
export class ListingProvider {
    listings: Listing[];
    myListings: Listing[];

    constructor(public http: Http,
                public kasperService: KasperService,
                private _logger: Logger) {
        this.listings = [];
        this.myListings = [];
    }

    /**
     * Add a listing to the database
     */
    addListing(newListing: Listing): any{
        assert.object(newListing, "Received a null listing");

        return this.kasperService.createListings(newListing);
    }

    /**
     * Edit an existing listing in the database
     */
    editListing(listingId: number, changeValues: {}){
        this._logger.error("ListingProvider.editListing is not implemented.");
        // return this.kasperService.editListing(listingId, changeValues);
    }

    /**
     * Remove a listing from the database
     *
     * @param listingId the id of the listing
     */
    removeListing(listingId : number){
        this._logger.error("ListingProvider.removeListing is not implemented.");
    }

    /**
     * Dislike a listing
     *
     * @param listingId the id of the listing
     */
    dislike(listingId : number): any{
        assert.number(listingId, "listingID must be a number.");
        // this._logger.error("ListingProvider.dislike is not implemented.");
        this.kasperService.likeDislikeListing(listingId, false);
    }

    likeDislikeCallback(){}

    /**
     * Add a listing to a users favourites
     *
     * @param listingId the id of the listing
     */
    addToFavourites(listingId : number): any{
        assert.number(listingId, "listingID must be a number.");
        // this._logger.error("ListingProvider.addToFavourites is not implemented.");
        return this.kasperService.likeDislikeListing(listingId, true);
    }

    /**
     * Remove a listing from a users favourites
     *
     * @param listingID the id of the listing
     */
    removeFromFavourites(listingId : number){
        this._logger.error("ListingProvider.removeFromFavourites is not implemented.");
    }

    /**
     * Search the database according to the specified filter
     *
     * @param filter the filter for the search
     *
     * @return an array of listingIDs
     */
    search(filter : Filter) : any{
        this._logger.error("ListingProvider.search is not implemented.");
        return null;
    }

    /**
     * Get the full information about a listing
     *
     * @param filter            the filter to apply to the search
     * @param requiredFields    the fields we want returned from the server
     * @param limit             the max number of returned results
     * @return a listing
     */
    getListings(filter: Filter, requiredFields: string[], limit: number) : any{
        return this.kasperService.getListings(filter, requiredFields, limit);
    }

    /**
     * Get the full information about a listing
     *
     * @return an array of listings
     */
    getMyListings() : any{
        return this.kasperService.getMyListings();
    }

    /**
     * Get the full information about a listing
     *
     * @return an array of listings
     */
    getFavourites() : any{
        return this.kasperService.getFavourites();
    }

    /**
     * Publish a listing
     *
     * @param listingId the id of the listing
     */
    publishListing(listingId : number): any{
        this._logger.error("ListingProvider.publishListing is not implemented.");
        return this.editListing(listingId, {'isPublished': true});
    }

    /**
     * Unpublish a listing
     *
     * @param listingId the id of the listing
     */
    unpublishListing(listingId : number): any{
        this._logger.error("ListingProvider.unpublishListing is not implemented.");
        return this.editListing(listingId, {'isPublished': false});
    }
}


