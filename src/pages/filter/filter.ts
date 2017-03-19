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
    private _provinces: Province[];
    private _priceMin: number = 100000;
    private _priceMax: number = 1600000;
    private _squareFeetMin: number = 100;
    private _squareFeetMax: number = 10000;
    private _bedroomsMin: number = 1;
    private _bedroomsMax: number = 10;
    private _bathroomsMin: number = 1;
    private _bathroomsMax: number = 10;

    province: string;
    price: Bound = {lower: this._priceMin, upper: this._priceMax};
    squareFeet: Bound = {lower: this._squareFeetMin, upper: this._squareFeetMax};
    bedrooms: Bound = {lower: this._bedroomsMin, upper: this._bedroomsMax};
    bathrooms: Bound = {lower: this._bathroomsMin, upper: this._bathroomsMax};

    constructor(public viewCtrl: ViewController,
                public params: NavParams,
                private _logger: Logger) {

        this._provinces = Province.asArray;
        // If we're given a filter, load it, otherwise use default values
        if(params.get("filter"))
            this.loadFilter(params.get("filter"));
    }

    loadFilter(filter: Filter): void{
        this.province = (filter.province) ? filter.province.abbr : "";

        // If we're given a bound, use the bound, otherwise use the default.
        if(filter.price.upper)
            this.price.upper = filter.price.upper;
        if(filter.price.lower)
            this.price.lower = filter.price.lower;

        if(filter.squareFeet.lower)
            this.squareFeet.lower = filter.squareFeet.lower;
        if(filter.squareFeet.upper)
            this.squareFeet.upper = filter.squareFeet.upper;

        if(filter.bedrooms.lower)
            this.bedrooms.lower = filter.bedrooms.lower;
        if(filter.bedrooms.upper)
            this.bedrooms.upper = filter.bedrooms.upper;

        if(filter.bathrooms.lower)
            this.bathrooms.lower = filter.bathrooms.lower;
        if(filter.bathrooms.upper)
            this.bathrooms.upper = filter.bathrooms.upper;

        this._logger.debug("Loaded filter: " + JSON.stringify(filter));
    }

    /**
     * Close this modal and pass the filter data back
     */
    applyFilter(): void{
        // Turn the province strings into an array of provinces
        let province: Province = Province.fromAbbr(this.province);

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
            province, tempPrice, tempSquareFeet, tempBedrooms, tempBathrooms
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
