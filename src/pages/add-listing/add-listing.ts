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
    editMode: boolean;

    private listingId: number;
    private listerId: number;
    private modifiedDate: string;
    private createdDate: string;
    private isPublished: boolean;
    private longitude: number;
    private latitude: number;

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
            this.editMode = true;
        } else {
            this.loadListingInfo(Listing.emptyListing());
            this.editMode = false;
        }
    }

    loadListingInfo(listing: Listing): void{
        assert.object(listing, "listing should never be null");

        this.listingId = listing.listingId;
        this.listerId = listing.listerId;
        this.modifiedDate = listing.modifiedDate;
        this.createdDate = listing.createdDate;
        this.isPublished = listing.isPublished;
        this.longitude = listing.longitude;
        this.latitude = listing.latitude;
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
            targetWidth: 1280, //make it const in kasper config
            targetHeight: 720 //make it const in kasper config
        };

        Camera.getPicture(options).then((data) => {
            this.images[this.images.length] = data;
        }, (error) => {
            this._logger.error("An error occurred while selecting an image."); // can be one log
            this._logger.error(JSON.stringify(error));
        });
    }

    getCurListing(): Listing{
        return new Listing(
            this.listingId,
            this.listerId,
            this.bedrooms,
            this.bathrooms,
            this.squarefeet, //refactor
            this.price,
            this.description,
            this.isPublished,
            this.createdDate,
            this.modifiedDate,
            this.images,
            this.province,
            this.city,
            this.address,
            this.postalCode,
            this.latitude,
            this.longitude,
        );
    }

    saveListing(){
        if(this.editMode){
            this.updateListing();
        } else {
            this.addListing();
        }
    }

    addListing(){
        let result = this.listingProvider.addListing(this.getCurListing());

        result.subscribe(data => {
            this._logger.info("Data from addListing");
            this._logger.info(JSON.stringify(data));
        }, error => {
            this.listingProvider.kasperService.handleError("createListing", error.json());
        });

        this.navCtrl.pop();
    }

    updateListing(){
    }

    /**
     * Save the listing to the server 
     */
    saveWithoutPublishing(){
        this._logger.error("AddListingPage.saveWithoutPublishing"); // TODO: shouldnt be a log error
        this.isPublished = false;
        this.saveListing();
    }

    /**
     * Set the listing to published
     */
    //TODO: Remove
    saveAndPublish(){
        this._logger.error("AddListingPage.saveAndPublish is not implemented yet");
        this.isPublished = true;
        this.saveListing();
    }

    /**
     * Set the listing to unpublished
     */
    unpublish(){
        this._logger.error("AddListingPage.unpublish is not implemented yet");
    }
}
