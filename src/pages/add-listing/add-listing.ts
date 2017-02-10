import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController} from 'ionic-angular';
import {Camera} from 'ionic-native';

@Component({
    selector: 'page-add-listing',
    templateUrl: 'add-listing.html'
})
export class AddListingPage {
    bathrooms: number;
    province: string;
    city: string;
    bedrooms: number;
    squarefeet: number;
    price: number;
    address: string;
    description: string;
    images: string[];

    constructor(public navCtrl: NavController,
                private _logger: Logger) {

    }

    save(){

    }

    /**
     * Display the UI to add the image
     */
    addImage(){
        const options = {
            // Turn image to byte64
            destinationType: Camera.DestinationType.DATA_URL,
            // Pick image from library
            sourceType: Camera.PictureSourceType.PHOTOLIBRARY,
            // Dimensions to scale image to
            targetWidth: 1280,
            targetHeight: 720
        };

        Camera.getPicture(options).then((data) => {
            // This should be the byte64 representation of the image.
            console.log(data);
            // Add the data to the end of the images array.
            this.images[this.images.length] = data;
        }, (error) => {
            console.log(error);
        });
    }

    publish(){

    }
}
