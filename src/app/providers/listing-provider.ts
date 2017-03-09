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
    addListing(newListing: Listing){
        assert.object(newListing, "Received a null listing");

        this._logger.error("ListingProvider.addListing is not implemented.");
    }

    addListingCallback(data: any){}

    /**
     * Edit an existing listing in the database
     */
    editListing(){
        this._logger.error("ListingProvider.editListing is not implemented.");
        // this.kasperService.editListing(changeValues, this.editListingCallback);
    }

    editListingCallback(data: any){}

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
     * @param listingID the id of the listing
     */
    dislike(listingID : number){
        this._logger.error("ListingProvider.dislike is not implemented.");
        // this.kasperService.likeDislikeListing(listingID, false);
    }

    likeDislikeCallback(){}

    /**
     * Add a listing to a users favourites
     *
     * @param listingID the id of the listing
     */
    addToFavourites(listingID : number){
        this._logger.error("ListingProvider.addToFavourites is not implemented.");
        // this.kasperService.likeDislikeListing(listingID, true);
    }

    /**
     * Remove a listing from a users favourites
     *
     * @param listingID the id of the listing
     */
    removeFromFavourites(listingID : number){
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
     * @param listingID
     * @return a listing
     */
    getListings() : void{
        this._logger.error("ListingProvider.getListing is not implemented.");
        return null;
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
     * @param listingID the id of the listing
     */
    publishListing(listingID : number){
        this._logger.error("ListingProvider.publishListing is not implemented.");
    }

    /**
     * Unpublish a listing
     *
     * @param listingID the id of the listing
     */
    unpublishListing(listingID : number){
        this._logger.error("ListingProvider.unpublishListing is not implemented.");
    }
}


