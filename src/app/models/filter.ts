import {Province} from "./province";
import {Bound} from "./bound";

/**
 * Outlines a basic filter object
 */
export class Filter{
    public provinces: Province[];
    public price: Bound;
    public squareFeet: Bound;
    public bedrooms: Bound;
    public bathrooms: Bound;

    constructor(provinces: Province[], price: Bound, squareFeet: Bound, bedrooms: Bound, bathrooms: Bound) {
        this.provinces = provinces;
        this.price = price;
        this.squareFeet = squareFeet;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
    }
}
