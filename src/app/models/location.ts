export class Location{
    public province: string;
    public city: string;
    public address: string;
    public postalCode: string;
    public long: number;
    public lat: number;

    constructor(province: string, city: string, address: string, postalCode: string, long: number,
                lat: number){
        this.province = province;
        this.city = city;
        this.address = address;
        this.postalCode = postalCode;
        this.long = long;
        this.lat = lat;
    }
}