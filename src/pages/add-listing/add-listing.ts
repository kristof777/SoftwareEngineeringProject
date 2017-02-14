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

    save(){
        let newLocation: Location = new Location(Province.fromAbbr(this.province), this.city, this.address,
            this.postalCode, 0.0, 0.0);

        let newListing: Listing = new Listing(-1, -1, newLocation, this.bedrooms, this.bathrooms, this.squarefeet,
            this.price, this.description, false, "0000-00-00", "0000-00-00", []);

        // TODO save to device

        // TODO save to server
        console.log("save button clicked")
        this.addListingToServer(newListing)
    }

    /**
     * Display the UI to add the image
     */
    addImage(){
        const options = {
            // Turn image to byte64
            destinationType: 0,//Camera.DestinationType.DATA_URL,
            // Pick image from library
            sourceType: 0,//Camera.PictureSourceType.PHOTOLIBRARY,
            // Dimensions to scale image to
            targetWidth: 1280,
            targetHeight: 720
        };

        Camera.getPicture(options).then((data) => {
            // data is the byte64 representation of the image selected
            // Add the data to the end of the images array.
            this.images[this.images.length] = data;
        }, (error) => {
            console.log(error);
        });
    }

    publish(){

    }

    /**
     * Call the method to create a new listing in the database
     * @param newListing
     */
    addListingToServer(newListing: Listing): void{
        console.log("addListingToServer function called.")
        this.listingProvider.addListing(newListing);
    }
}
