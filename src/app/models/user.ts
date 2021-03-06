import {UserSettings} from "./user-settings";
import {Province} from "./province";

export class User{
    public id: number;
    public email: string;
    public firstName: string;
    public lastName: string;
    public phone1: string;
    public phone2: string;
    public province: Province;
    public city: string;
    public location: Location;
    public settings: UserSettings;

    /**
     *  Creates a user
     *
     * @param id        unique identifier for the user
     * @param email     the user's email
     * @param firstName the user's first name
     * @param lastName  the user's last name
     * @param phone1    the user's primary phone number
     * @param phone2    the user's secondary phone number
     * @param province  the user's province
     * @param city      the user's city
     */
    constructor(id: number, email: string, firstName: string, lastName: string, phone1: string,
                phone2: string, province: Province, city: string) {
        this.id = id;
        this.email = email;
        this.firstName = firstName;
        this.lastName = lastName;
        this.phone1 = phone1;
        this.phone2 = phone2;
        this.province = province;
        this.city = city;
    }
}
