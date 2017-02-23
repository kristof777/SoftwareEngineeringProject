import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavParams, NavController, ViewController} from 'ionic-angular';
import {Filter} from "../../app/models/filter";
import {Bound} from "../../app/models/bound";
import {Province} from "../../app/models/province";

@Component({
    selector: 'page-filter',
    templateUrl: 'filter.html'
})
export class FilterPage {
    // ngModel binds the value of the html element to variable "province"
    // to access use this.province
    province: string[];
    minPrice: any = 275000;
    maxPrice: any = 300000;
    squareFeet: Bound = {lower: 1400, upper: 2000};
    bedrooms: Bound = {lower: 1, upper: 4};
    bathrooms: Bound = {lower: 2, upper: 3};

    // Creates the logger object (needed in all constructors
    constructor(public viewCtrl: ViewController,
                params: NavParams,
                private _logger: Logger) {
    }

    /**
     * Close this modal and pass the filter data back
     */
    applyFilter(): void{
        // Turn the province strings into an array of provinces
        let provinces: Province[] = [];
        if(this.province && this.province.length > 0) {
            for (let i = 0; i < this.province.length; i++)
                provinces.push(Province.fromAbbr(this.province[i]));
        }

        let data: Filter = new Filter(
            provinces,
            {lower: this.minPrice, upper: this.maxPrice},
            this.squareFeet, this.bedrooms, this.bathrooms
        );

        this.viewCtrl.dismiss(data);
    }

    /**
     * Close this modal and don't pass data back
     */
    cancel(): void{
        this.viewCtrl.dismiss();
    }
}
