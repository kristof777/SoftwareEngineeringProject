import {User} from "../../app/models/user";
import {ListingProvider} from "../../app/providers/listing-provider";
import {Component, ViewChild} from "@angular/core";
import {NavController, ModalController, NavParams, Slides} from "ionic-angular";
import {Listing} from "../../app/models/listing";
import {Logger} from "angular2-logger/core";
import {LoginService} from "../../app/providers/login-service";
import {Province} from "../../app/models/province";
import {Location} from "../../app/models/location";
import {AddListingPage} from "../add-listing/add-listing";
import {ContactPage} from "../contact/contact";
let assert = require('assert-plus');

@Component({
    selector: 'page-detail',
    templateUrl: 'detail.html',
    providers: [ListingProvider]
})
export class DetailPage {
    @ViewChild(Slides) slides: Slides;
    data: Listing[];
    // The index of the page currently being displayed
    cursor: number = 0;

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                public listings: ListingProvider,
                public loginService: LoginService,
                private _logger: Logger,
                public navParams: NavParams) {
        if(Object.keys(navParams.data).length === 0 && navParams.data.constructor === Object) {
            this.data = listings.data;
        } else {
            this.data = navParams.get('data');
            this.cursor = navParams.get('cursor');
        }

        //TODO: Remove fake user account
        let userID: number = 1;
        let email: string = "john.doe@gmail.com";
        let firstName: string = "John";
        let lastName: string = "Doe";
        let phone1: string = "3065555555";
        let phone2: string = null;
        let location: Location = new Location(Province.SK, "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0);

        this.loginService.setUser(new User(userID, email, firstName, lastName, phone1, phone2, location));
    }


    /**
     * Navigate to the My Listings page.
     */
    goToFavourites(): void{
        this._logger.debug("Favourites was clicked");
    }

    /**
     * Add the house to the users dislike list
     */
    unlike(): void{
        this._logger.debug("Unlike was clicked");
    }

    /**
     * Add the house to the users favourites list
     */
    like(): void{
        this._logger.debug("Like was clicked.");
    }

    /**
     * Return to the first image in the slides
     */
    goToFirstSlide(): void{
        this.slides.slideTo(0, 0);
    }

    /**
     * Display the next property
     */
    nextProperty(): void{
        this._logger.debug("Next Property was clicked");

        this.goToFirstSlide();

        if(this.isNextProperty())
            this.cursor += 1;
    }

    /**
     * Display the previous property
     */
    previousProperty(): void{
        this._logger.debug("Previous Property was clicked");

        this.goToFirstSlide();

        if(this.isPreviousProperty())
            this.cursor -= 1;
    }

    /**
     * Edit the current property
     */
    edit(): void{
        this.navCtrl.push(
            AddListingPage, { listing: this.data[this.cursor] }
        );
    }

    /**
     * Check if there is a property before the current.
     *
     * @returns {boolean}   true if there is a property before this one
     */
    isPreviousProperty(): boolean{
        return this.cursor > 0;
    }

    /**
     * Check if there is a property after the current.
     *
     * @returns {boolean}   true if there is a property afterhis one
     */
    isNextProperty(): boolean{
        return this.cursor < (this.data.length - 1);
    }

    /**
     * Check if the current property belongs to the logged in user
     *
     * @returns {boolean}   true if it is their property
     */
    belongsToUser(): boolean{
        return this.loginService.getUserId() == this.data[this.cursor].listerId;
    }

    goToContact(): void{
        this.navCtrl.push(ContactPage, {listingId: this.data[this.cursor].listingId});
    }
}
