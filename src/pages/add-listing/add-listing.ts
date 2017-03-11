import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController, NavParams} from 'ionic-angular';
import {Camera} from 'ionic-native';
import {Listing} from "../../app/models/listing";
import {ListingProvider} from "../../app/providers/listing-provider";
import {Province} from "../../app/models/province";

@Component({
    selector: 'page-add-listing',
    templateUrl: 'add-listing.html',
    providers: [ListingProvider]
})
export class AddListingPage {
    curListing: Listing;

    private listingId;
    private listerId;
    bathrooms: number;
    province: string;
    city: string;
    bedrooms: number;
    squarefeet: number;
    price: number;
    address: string;
    postalCode: string;
    description: string;
    images: string[];

    constructor(public navCtrl: NavController,
                public listingProvider: ListingProvider,
                public navParams: NavParams,
                private _logger: Logger) {
        this.images = [];

        if(this.navParams.get('listing')){
            this.loadListingInfo(this.navParams.get('listing'));
        }
    }

    loadListingInfo(listing: Listing): void{
        assert.object(listing, "listing should never be null");

        this.curListing = new Listing(
            listing.listingId,
            listing.listerId,
            listing.bedrooms,
            listing.bathrooms,
            listing.squarefeet,
            listing.price,
            listing.description,
            listing.isPublished,
            listing.createdDate,
            listing.modifiedDate,
            listing.images,
            Province.fromAbbr(listing.province.abbr),
            listing.city,
            listing.address,
            listing.postalCode,
            listing.latitude,
            listing.longitude,
        );

        this.listingId = listing.listingId;
        this.listerId = listing.listerId;
        this.bathrooms = listing.bathrooms;
        this.province = listing.province.abbr;
        this.city = listing.city;
        this.bedrooms = listing.bedrooms;
        this.squarefeet = listing.squarefeet;
        this.price = listing.price;
        this.address = listing.address;
        this.postalCode = listing.postalCode;
        this.description = listing.description;
        this.images = listing.images;
    }

    /**
     * Display the UI to add the image
     */
    addImage(){
        const options = {
            // Get image in byte64
            destinationType: 0,//Camera.DestinationType.DATA_URL,
            // Pick image from library
            sourceType: 0,//Camera.PictureSourceType.PHOTOLIBRARY,
            // Dimensions to scale the image to
            targetWidth: 1280,
            targetHeight: 720
        };

        Camera.getPicture(options).then((data) => {
            this.images[this.images.length] = data;
        }, (error) => {
            this._logger.error("An error occurred while selecting an image.");
            this._logger.error(JSON.stringify(error));
        });
    }

    /**
     * Save the listing to the device and the server
     */
    saveWithoutPublishing(){
        this._logger.error("AddListingPage.saveWithoutPublishing is not implemented yet");
    }

    /**
     * Set the listing to published
     */
    saveAndPublish(){
        this._logger.error("AddListingPage.saveAndPublish is not implemented yet");
    }

    /**
     * Set the listing to unpublished
     */
    unpublish(){
        this._logger.error("AddListingPage.unpublish is not implemented yet");
    }
}
