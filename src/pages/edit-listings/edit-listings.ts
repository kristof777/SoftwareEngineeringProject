import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';
import {NavController, NavParams} from 'ionic-angular';
@Component({
    selector: 'page-edit-listings',
    templateUrl: 'edit-listings.html'
})
export class EditListingsPage {

    bathrooms: number;
    province: string;
    city: string;
    bedrooms: number;
    squarefeet: number;
    price: number;
    address: string;
    postalCode: string;
    description: string;

    constructor(public navCtrl: NavController,
                private _logger: Logger,
                public navparams: NavParams) {
        let listing = navparams.get("data");
        this.bathrooms = listing['bathrooms'];
        this.province = listing['location']['province'];
        this.bedrooms = listing['bedrooms'];
        this.squarefeet = listing['squarefeet'];
        this.price = listing['price'];
        this.address = listing['location']['address'];
        this.description = listing['description'];
        this.city = listing['location']['city'];

    }

        save(){

        }

        editimage(){

        }

        publish(){

        }

}
