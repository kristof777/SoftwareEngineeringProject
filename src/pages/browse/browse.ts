import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from "@angular/core";
import {NavController, ModalController, ItemSliding, ToastController} from "ionic-angular";
import {Logger} from "angular2-logger/core";
import {Listing} from "../../app/models/listing";
import {FilterPage} from "../filter/filter";
import {DetailPage} from "../detail/detail";
import {Filter} from "../../app/models/filter";
let assert = require('assert-plus');

@Component({
    selector: 'page-browse',
    templateUrl: 'browse.html',
    providers: [ListingProvider]
})
export class BrowsePage {
    listings: Listing[];
    voteDelay: number = 1000;
    canVote: boolean = true;

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
        if(!this.canVote) return;
        if (event.getOpenAmount() < -100) {
            this.likeListing(index);
        } else if (event.getOpenAmount() > 100) {
            this.dislikeListing(index);
        }
    }

    /**
     * Send request to dislike a listing
     *
     * @param index the index of the listing
     */
    dislikeListing(index: number): void{
        assert(index > -1 && index < this.listings.length,
            "Index should be within the bounds of available listings");

        this.startVoteTimer();

        this._logger.debug("Disliking slide at index " + index);

        this.toastCtrl.create({
            message: "Disliked the selected listing.",
            duration: 3000,
            position: 'top'
        }).present();

        this.listings.splice(index, 1);
    }

    /**
     * Send request to like a listing
     *
     * @param index the index of the listing
     */
    likeListing(index: number): void{
        assert(index > -1 && index < this.listings.length,
            "Index should be within the bounds of available listings");

        this.startVoteTimer();

        this._logger.debug("Liking slide at index " + index);

        this.toastCtrl.create({
            message: "Liked the selected listing.",
            duration: 3000,
            position: 'top'
        }).present();

        this.listings.splice(index, 1);
    }

    /**
     * Display the filters screen
     */
    goToFilters(): void{
        this._logger.debug("Filters was clicked");

        let filterModal = this.modalCtrl.create(FilterPage, { filter: null });

        filterModal.onDidDismiss((data: Filter) => {
            if(!data){
                this._logger.debug("Filter Modal was cancelled");
            } else {
                this._logger.debug("Filter Modal Data: " + JSON.stringify(data));
            }
        });

        filterModal.present();
    }

    /**
     * Open the detailed page of a listing
     * @param index the index of the listing
     */
    goToDetails(index): void{
        assert(index > -1 && index < this.listings.length,
            "Index should be within the bounds of available listings");

        this.navCtrl.push(DetailPage, {data: this.listings, cursor: index});
    }

    /**
     * Set a delay for voting
     */
    startVoteTimer(): void{
        let me = this;
        this.canVote = false;
        setTimeout(function(){
            me.canVote = true;
        }, this.voteDelay);
    }
}
