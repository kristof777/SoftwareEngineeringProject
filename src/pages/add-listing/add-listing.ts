import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Camera} from 'ionic-native';
import {Listing} from "../../app/models/listing";
import {ListingProvider} from "../../app/providers/listing-provider";
import {Location} from "../../app/models/location";
import {Province} from "../../app/models/province";

@Component({
    selector: 'page-add-listing',
    templateUrl: 'add-listing.html',
    providers: [ListingProvider]
})
export class AddListingPage {
    curListing: Listing;
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
                private _logger: Logger) {
        this.images = [];
    }

    /**
     * Returns true if all of the required fields are present
     */
    verifyFields(): boolean{
        return false;
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
            this._logger.log(error);
        });
    }

    /**
     * Save the listing to the device and the server
     */
    saveWithoutPublishing(){
        let newListing: Listing = new Listing(
            -1, -1, // listingId, listerId
            new Location(Province.fromAbbr(this.province), this.city, this.address, this.postalCode,
                0.0, 0.0), // longintude, latitude
            this.bedrooms, this.bathrooms, this.squarefeet, this.price, this.description,
            false, "0000-00-00", "0000-00-00", // isPublished, created, modified
            this.images,
        );

        this.listingProvider.addListing(newListing);
    }

    /**
     * Set the listing to published
     */
    saveAndPublish(){}

    /**
     * Set the listing to unpublished
     */
    unpublish(){}
}
