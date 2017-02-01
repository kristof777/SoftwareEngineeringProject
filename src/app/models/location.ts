import {Province} from "./province";

export class Location{
    public province: Province;
    public city: string;
    public address: string;
    public postalCode: string;
    public long: number;
    public lat: number;

    constructor(province: Province, city: string, address: string, postalCode: string, long: number,
                lat: number){
        this.province = province;
        this.city = city;
        this.address = address;
        this.postalCode = postalCode;
        this.long = long;
        this.lat = lat;
    }
}
