export class ListingModel {
    constructor(public id: number, // id of the listing
                public lister: number, // id of the user who added this listing
                public location: string,
                public address: string, // location and address will be put into another data structure
                public bedrooms: number,
                public bathrooms: number,
                public squarefeet: number,
                public price: number,
                public description: string,
                public isHidden: boolean, // whether or not the listing will appear to others
                public createDate: string,
                public modifiedDate: string,
                public images: string[] // array of images
    ){}
}