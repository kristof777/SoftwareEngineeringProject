import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController} from 'ionic-angular';

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
    description: string;

    constructor(public navCtrl: NavController,
                private _logger: Logger) {

        }

        save(){

        }

        editimage(){

        }

        publish(){

        }

}
