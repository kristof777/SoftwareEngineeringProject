import {Location} from './location';

export class User{
    public id: number
    public email: string;
    public firstName: string;
    public lastName: string;
    public phone1: string;
    public phone2: string;
    public location: Location;

    /**
     *
     * @param id
     * @param email
     * @param firstName
     * @param lastName
     * @param phone1
     * @param phone2
     * @param location
     */
    constructor(id: number, email: string, firstName: string, lastName: string, phone1: string,
                phone2: string, location: Location) {
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.phone1 = phone1;
        this.phone2 = phone2;
        this.location = location;
    }
}
