import {ListingProvider} from "../../app/providers/listing-provider";
let assert = require('assert-plus');
import {Component, ViewChild} from '@angular/core';

import {NavController, ToastController, ModalController, NavParams, Slides} from 'ionic-angular';

import {Listing} from '../../app/models/listing';
import {FilterPage} from '../filter/filter';
import {Logger} from "angular2-logger/core";

@Component({
    selector: 'page-browse',
    templateUrl: 'browse.html',
    providers: [ListingProvider]
})
export class BrowsePage {
    @ViewChild(Slides) slides: Slides;
    data: Listing[];
    // The index of the page currently being displayed
    cursor: number = 0;

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                public modalCtrl: ModalController,
                public listings: ListingProvider,
                private _logger: Logger) {
        this.data = listings.data;
    }

    goToFavourites(){
        this._logger.debug("Favourites was clicked");
    }

    goToFilters(){
        this._logger.debug("Filters was clicked");
        let filterModal = this.modalCtrl.create(FilterPage, { someData: "data" });

        filterModal.onDidDismiss(data => {
            this._logger.debug("Filter Modal Data: " + JSON.stringify(data));
        });

        filterModal.present();
    }

    unlike(){
        this._logger.debug("Unlike was clicked");
    }

    like(){
        this._logger.debug("Like was clicked.");
    }

    goToFirstSlide(){
        this.slides.slideTo(0, 0);
    }

    nextProperty(){
        this.goToFirstSlide();
        this._logger.debug("Next Property was clicked");
        if(this.cursor < (this.data.length - 1))
            this.cursor += 1;
    }

    previousProperty(){
        this.goToFirstSlide();
        this._logger.debug("Previous Property was clicked");
        if(this.cursor > 0)
            this.cursor -= 1;
    }
}
