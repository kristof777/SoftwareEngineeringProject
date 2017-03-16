import {Province} from "./province";

export class Listing {
    public listingId: number;
    public listerId: number;
    public bedrooms: number;
    public bathrooms: number;
    public squarefeet: number;
    public price: number;
    public description: string;
    public isPublished: boolean;
    public createdDate: string;
    public modifiedDate: string;
    public images: string[];

    public province: Province;
    public city: string;
    public address: string;
    public postalCode: string;
    public longitude: number;
    public latitude: number;

    /**
     * Creates a listing
     *
     * @param listingId     id of the listing
     * @param listerId      id of the user who listed this listing
     * @param bedrooms      the amount of bedrooms
     * @param bathrooms     the amount of bathrooms
     * @param squarefeet    the square feet
     * @param price         the price
     * @param description   a description
     * @param isPublished   whether or not thie listing will appear on the browse page
     * @param createdDate   the date this listing was created
     * @param modifiedDate  the last time this listing was modified
     * @param images        an array of images in byte64
     * @param province      the abbreviation of the province of the listing
     * @param city          the city of the listing
     * @param address       the address of the listing
     * @param postalCode    the postal code of the listing
     * @param longitude     the longitude of the listing
     * @param latitude      the latitude of the listing
     */
    constructor(listingId: number, listerId: number, bedrooms: number,
                bathrooms: number, squarefeet: number, price: number, description: string,
                isPublished: boolean, createdDate: string, modifiedDate: string,
                images: string[], province: string, city: string, address: string,
                postalCode: string, longitude: number, latitude: number) {
        this.listingId = listingId;
        this.listerId = listerId;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
        this.squarefeet = squarefeet;
        this.price = price;
        this.description = description;
        this.isPublished = isPublished;
        this.createdDate = createdDate;
        this.modifiedDate = modifiedDate;
        this.images = images;

        this.province = Province.fromAbbr(province);
        this.city = city;
        this.address = address;
        this.postalCode = postalCode;
        this.longitude = longitude;
        this.latitude = latitude;
    }

    static emptyListing(): Listing{
        return new Listing(-1, -1, 0, 0, 0, 0, "", false, "0000-00-00", "0000-00-00", [],
            "SK", "", "", "", 0.0, 0.0);
    }
}
