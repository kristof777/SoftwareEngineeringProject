import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController, NavParams} from 'ionic-angular';
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
        assert.object(listing);

        this.listingId = listing.listingId;
        this.listerId = listing.listerId;
        this.bathrooms = listing.bathrooms;
        this.province = listing.location.province.abbr;
        this.city = listing.location.city
        this.bedrooms = listing.bedrooms;
        this.squarefeet = listing.squarefeet;
        this.price = listing.price;
        this.address = listing.location.address;
        this.postalCode = listing.location.postalCode;
        this.description = listing.description;
        this.images = listing.images;
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
            new Location(((this.province) ? Province.fromAbbr(this.province) : null), this.city, this.address,
                this.postalCode, 0.0, 0.0), // longintude, latitude
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
