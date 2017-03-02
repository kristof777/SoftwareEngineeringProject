import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from "@angular/core";
import {NavController, ModalController, ItemSliding, ToastController} from "ionic-angular";
import {Logger} from "angular2-logger/core";
import {Listing} from "../../app/models/listing";
import {FilterPage} from "../filter/filter";
import {DetailPage} from "../detail/detail";
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

    /**
     * Called when the user drags a listing
     *
     * @param event the drag event
     * @param index the index of the listing being dragged
     */
    onDrag(event: ItemSliding, index: number){
        if(event.getOpenAmount() < -100){
            this.likeListing(index);
        } else if (event.getOpenAmount() > 100){
            this.dislikeListing(index);
        }
    }

    /**
     * Send request to dislike a listing
     *
     * @param index the index of the listing
     */
    dislikeListing(index: number): void{
        this._logger.log("Disliking slide at index " + index);

        this.toastCtrl.create({
            message: "Disliked the selected listing.",
            duration: 3000,
            position: 'top'
        }).present();

        delete this.listings[index];
    }

    /**
     * Send request to like a listing
     *
     * @param index the index of the listing
     */
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

    /**
     * Open the detailed page of a listing
     * @param index the index of the listing
     */
    goToDetails(index): void{
        this.navCtrl.push(DetailPage, {data: this.listings, cursor: index});
    }
}
