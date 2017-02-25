import {ListingProvider} from "../../app/providers/listing-provider";
import {Component, ViewChild} from "@angular/core";
import {NavController, ModalController, ItemSliding, ToastController} from "ionic-angular";
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
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                public listingProvider: ListingProvider,
                public modalCtrl: ModalController,
                private _logger: Logger,) {

        this.listings = listingProvider.data;
    }

    onDrag(event: ItemSliding, index: number){
        if(event.getOpenAmount() < -100){
            this.likeListing(index);
        } else if (event.getOpenAmount() > 100){
            this.dislikeListing(index);
        }
    }

    dislikeListing(index: number): void{
        this._logger.log("Disliking slide at index " + index);

        this.toastCtrl.create({
            message: "Disliked the selected listing.",
            duration: 3000,
            position: 'top'
        }).present();

        delete this.listings[index];
    }

    likeListing(index: number): void{
        this._logger.log("Liking slide at index " + index);

        this.toastCtrl.create({
            message: "Liked the selected listing.",
            duration: 3000,
            position: 'top'
        }).present();

        delete this.listings[index];
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
