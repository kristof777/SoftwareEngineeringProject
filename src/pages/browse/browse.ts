import {ListingProvider} from "../../app/providers/listing-provider";
import {Component, ViewChild} from "@angular/core";
import {NavController, ModalController, Slides} from "ionic-angular";
import {Logger} from "angular2-logger/core";
import {Listing} from "../../app/models/listing";
import {FilterPage} from "../filter/filter";
let assert = require('assert-plus');

@Component({
    selector: 'page-browse',
    templateUrl: 'browse.html',
    providers: [ListingProvider]
})
export class BrowsePage {
    @ViewChild(Slides) slides: Slides;
    listing: Listing;

    constructor(public navCtrl: NavController,
                public listingProvider: ListingProvider,
                public modalCtrl: ModalController,
                private _logger: Logger,) {

        this.listing = listingProvider.data[0];
    }

    onSlideChange(currentListing): void{
        console.log("Slide changed");
        if(this.slides.isBeginning()){
            this.likeCurrent();
        } else if(this.slides.isEnd()){
            this.dislikeCurrent();
        }
    }

    dislikeCurrent(): void{
        this._logger.log("Disliking the current slide");
    }

    likeCurrent(): void{
        this._logger.log("Liking the current slide");
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
}
