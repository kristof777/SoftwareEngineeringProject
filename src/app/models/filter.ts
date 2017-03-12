import {Province} from "./province";
import {Bound} from "./bound";

/**
 * Outlines a basic filter object
 */
export class Filter{
    public province: Province;
    public price: Bound;
    public squarefeet: Bound;
    public bedrooms: Bound;
    public bathrooms: Bound;

    constructor(province: Province, price: Bound, squarefeet: Bound, bedrooms: Bound, bathrooms: Bound) {
        this.province = province;
        this.price = price;
        this.squarefeet = squarefeet;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
    }

    toJson(): string{
        let temp: any = JSON.parse(JSON.stringify(this));

        if(this.province)
            temp.province = this.province.abbr;
        else
            delete temp.province;

        return JSON.stringify(temp);
    }
}
