import {ListingProvider} from "../../app/providers/listing-provider";
import {Component, ViewChild} from "@angular/core";
import {NavController, ModalController, NavParams, Slides} from "ionic-angular";
import {Listing} from "../../app/models/listing";
import {Logger} from "angular2-logger/core";
import {LoginService} from "../../app/providers/login-service";
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
    cursor: number = 0;

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                public listingProvider: ListingProvider,
                public loginService: LoginService,
                private _logger: Logger,
                public navParams: NavParams) {
        if(Object.keys(navParams.data).length === 0 && navParams.data.constructor === Object) {
            this.data = listingProvider.listings;
        } else {
            this.data = navParams.get('data');
            this.cursor = navParams.get('cursor');
            this._logger.info(this.data);
            this._logger.info(this.data[this.cursor]);
        }
    }

    /**
     * Add the house to the users dislike list
     */
    dislike(): void{
        this._logger.debug("Dislike was clicked");
        this.listingProvider.dislikeListing(this.data[this.cursor].listingId).subscribe(data => {
            this._logger.debug("Dislike was successful.");
        }, error => {
            this.listingProvider.kasperService.handleError("likeDislikeListing", error.toJson());
        });
    }

    /**
     * Add the house to the users favourites list
     */
    like(): void{
        this._logger.debug("Like was clicked.");
        this.listingProvider.likeListing(this.data[this.cursor].listingId).subscribe(data => {
            this._logger.debug("Like was successful.");
        }, error => {
            this.listingProvider.kasperService.handleError("likeDislikeListing", error.toJson());
        });
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
        if(!this.loginService.isLoggedIn())
            return false;

        return this.loginService.getUserId() == this.data[this.cursor].listerId;
    }

    goToContact(): void{
        this.navCtrl.push(ContactPage, {listingId: this.data[this.cursor].listingId});
    }
}
