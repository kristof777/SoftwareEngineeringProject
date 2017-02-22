import {ListingProvider} from "../../app/providers/listing-provider";
let assert = require('assert-plus');
import {Component, ViewChild} from '@angular/core';
import {NavController, ToastController, ModalController, NavParams, Slides} from 'ionic-angular';
import {Listing} from '../../app/models/listing';
import {FilterPage} from '../filter/filter';
import {Logger} from "angular2-logger/core";

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
                public toastCtrl: ToastController,
                public modalCtrl: ModalController,
                public listings: ListingProvider,
                private _logger: Logger,
                public navParams: NavParams) {
        if(Object.keys(navParams.data).length === 0 && navParams.data.constructor === Object) {
            this.data = listings.data;
        }
        else {
            this.data = navParams.get('data');
            this.cursor = navParams.get('cursor');
        }
    }


    /**
     * Navigate to the My Listings page.
     */
    goToFavourites(): void{
        this._logger.info("Favourites was clicked");
    }

    /**
     * Display the filters screen
     */
    goToFilters(): void{
        this._logger.info("Filters was clicked");
        let filterModal = this.modalCtrl.create(FilterPage, { someData: "data" });

        filterModal.onDidDismiss(data => {
            this._logger.info("Filter Modal Data: " + JSON.stringify(data));
        });

        filterModal.present();
    }

    /**
     * Add the house to the users dislike list
     */
    unlike(): void{
        this._logger.info("Unlike was clicked");
    }

    /**
     * Add the house to the users favourites list
     */
    like(): void{
        this._logger.info("Like was clicked.");
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
        this.goToFirstSlide();
        this._logger.info("Next Property was clicked");
        if(this.cursor < (this.data.length - 1))
            this.cursor += 1;
    }

    /**
     * Display the previous property
     */
    previousProperty(): void{
        this.goToFirstSlide();
        this._logger.info("Previous Property was clicked");
        if(this.cursor > 0)
            this.cursor -= 1;
    }
}
