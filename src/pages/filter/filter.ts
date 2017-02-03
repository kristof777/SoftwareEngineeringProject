import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavParams, NavController, ViewController} from 'ionic-angular';

@Component({
    selector: 'page-filter',
    templateUrl: 'filter.html'
})
export class FilterPage {
    // ngModel binds the value of the html element to variable "province"
    // to access use this.province
    province: string;
    minPrice: any = 275000;
    maxPrice: any = 300000;
    squareFeet: any = {lower: 1400, upper: 2000};
    bedrooms: any = {lower: 1, upper: 4};
    bathrooms: any = {lower: 2, upper: 3};

    // Creates the logger object (needed in all constructors
    constructor(public viewCtrl: ViewController,
                params: NavParams,
                private _logger: Logger) {
    }

    /**
     * Close this modal and pass the filter data back
     */
    applyFilter(){
        let data = {
            province: this.province,
            minPrice: this.minPrice,
            maxPrice: this.maxPrice,
            minSquareFeet: this.squareFeet.lower,
            maxSquareFeet: this.squareFeet.upper,
            minBedrooms: this.bedrooms.lower,
            maxBedrooms: this.bedrooms.upper,
            minBathrooms: this.bathrooms.lower,
            maxBathrooms: this.bathrooms.upper
        };

        this.viewCtrl.dismiss(data);
    }

    /**
     * Close this modal and don't pass data back
     */
    cancel(){
        this.viewCtrl.dismiss();
    }
}
