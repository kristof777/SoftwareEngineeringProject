import {Province} from "./province";

export class Location{
    public province: Province;
    public city: string;
    public address: string;
    public postalCode: string;
    public longitude: number;
    public latitude: number;

    constructor(province: Province, city: string, address: string, postalCode: string,
                longitude: number, latitude: number){
        this.province = province;
        this.city = city;
        this.address = address;
        this.postalCode = postalCode;
        this.longitude = longitude;
        this.latitude = latitude;
    }
}
