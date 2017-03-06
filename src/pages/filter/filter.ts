import {Logger} from "angular2-logger/core";
import {Component} from "@angular/core";
import {NavParams, ViewController} from "ionic-angular";
import {Filter} from "../../app/models/filter";
import {Bound} from "../../app/models/bound";
import {Province} from "../../app/models/province";
let assert = require('assert-plus');

@Component({
    selector: 'page-filter',
    templateUrl: 'filter.html'
})
export class FilterPage {
    private _priceMin = 100000;
    private _priceMax = 1600000;
    private _squareFeetMin = 100;
    private _squareFeetMax = 10000;
    private _bedroomsMin = 1;
    private _bedroomsMax = 10;
    private _bathroomsMin = 1;
    private _bathroomsMax = 10;

    // ngModel binds the value of the html element to variable "province"
    // to access use this.province
    province: string[];
    price: Bound = {lower: 100000, upper: 1600000};
    squareFeet: Bound = {lower: 100, upper: 10000};
    bedrooms: Bound = {lower: 1, upper: 10};
    bathrooms: Bound = {lower: 1, upper: 10};

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

        let tempPrice: Bound = {};
        if(this.price.lower != this._priceMin) tempPrice['lower'] = this.price.lower;
        if(this.price.upper != this._priceMax) tempPrice['upper'] = this.price.upper;

        let tempSquareFeet: Bound = {};
        if(this.squareFeet.lower != this._squareFeetMin) tempSquareFeet['lower'] = this.squareFeet.lower;
        if(this.squareFeet.upper != this._squareFeetMax) tempSquareFeet['upper'] = this.squareFeet.upper;

        let tempBedrooms: Bound = {};
        if(this.bedrooms.lower != this._bedroomsMin) tempBedrooms['lower'] = this.bedrooms.lower;
        if(this.bedrooms.upper != this._bedroomsMax) tempBedrooms['upper'] = this.bedrooms.upper;

        let tempBathrooms: Bound = {};
        if(this.bathrooms.lower != this._bathroomsMin) tempBathrooms['lower'] = this.bathrooms.lower;
        if(this.bathrooms.upper != this._bathroomsMax) tempBathrooms['upper'] = this.bathrooms.upper;

        let data: Filter = new Filter(
            provinces, tempPrice, tempSquareFeet, tempBedrooms, tempBathrooms
        );

        this.viewCtrl.dismiss(data);
    }

    /**
     * Close this modal and don't pass data back
     */
    cancel(): void{
        this.viewCtrl.dismiss(null);
    }
}
