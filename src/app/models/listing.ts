export class ListingModel {
    constructor(public id: number,
                public lister: number,
                public location: string,
                public address: string,
                public bedrooms: number,
                public bathrooms: number,
                public squarefeet: number,
                public price: number,
                public description: string,
                public isHidden: boolean,
                public createDate: string,
                public modifiedDate: string,
                public images: string[]){}
}