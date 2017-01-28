import {Location} from "./location";

export class Listing {
    public listingId: number;
    public lister: number;
    public location: Location;
    public bedrooms: number;
    public bathrooms: number;
    public squarefeet: number;
    public price: number;
    public description: string;
    public isPublished: boolean;
    public createDate: string;
    public modifiedDate: string;
    public thumbnail: string;
    public images: string[];

    /**
     * Create a listing
     * @param listingId     id of the listing
     * @param lister        id of the user who listed this listing
     * @param location      the province and city
     * @param bedrooms      the amount of bedrooms
     * @param bathrooms     the amount of bathrooms
     * @param squarefeet    the square feet
     * @param price         the price
     * @param description   a description
     * @param isPublished   whether or not thie listing will appear on the browse page
     * @param createDate    the date this listing was created
     * @param modifiedDate  the last time this listing was modified
     * @param thumbnail     a thumbnail in byte64
     * @param images        an array of images in byte64
     */
    constructor(listingId: number, lister: number, location: Location, bedrooms: number,
                bathrooms: number, squarefeet: number, price: number, description: string,
                isPublished: boolean, createDate: string, modifiedDate: string,
                thumbnail: string, images: string[]) {
        this.listingId = listingId;
        this.lister = lister;
        this.location = location;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
        this.squarefeet = squarefeet;
        this.price = price;
        this.description = description;
        this.isPublished = isPublished;
        this.createDate = createDate;
        this.modifiedDate = modifiedDate;
        this.thumbnail = thumbnail;
        this.images = images;
    }
}