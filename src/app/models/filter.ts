import {Province} from "./province";
import {Bound} from "./bound";

/**
 * Outlines a basic filter object
 */
export class Filter{
    public province: Province;
    public price: Bound;
    public squareFeet: Bound;
    public bedrooms: Bound;
    public bathrooms: Bound;

    constructor(province: Province, price: Bound, squareFeet: Bound, bedrooms: Bound, bathrooms: Bound) {
        this.province = province;
        this.price = price;
        this.squareFeet = squareFeet;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
    }

    /**
     * Returns a JSON representation of the filter
     *
     * @returns {string} the filter as a JSON string
     */
    toJson(): string{
        let temp: any = JSON.parse(JSON.stringify(this));

        if(this.province)
            temp.province = this.province.abbr;
        else
            delete temp.province;

        return JSON.stringify(temp);
    }
}
