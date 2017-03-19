import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from "@angular/core";
import {NavController} from "ionic-angular";
import {Listing} from "../../app/models/listing";
import {Logger} from "angular2-logger/core";
import {DetailPage} from "../detail/detail";
import {LoginService} from "../../app/providers/login-service";
import {KasperService} from "../../app/providers/kasper-service";
let assert = require('assert-plus');

@Component({
    selector: 'page-favourites',
    templateUrl: 'favourites.html',
    providers: [ListingProvider]

})
export class FavouritesPage {
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public listingProvider: ListingProvider,
                public loginService: LoginService,
                private _logger: Logger) {

        this.listings = Array();
    }

    /**
     * Reload the users favourites when they open the page.
     *
     * TODO make this more efficient
     */
    ionViewDidEnter(){
        let me = this;

        if(this.loginService.isLoggedIn()) {
            this.listingProvider.getFavourites().subscribe(data => {
                me.listings = KasperService.fromData(data['listings']);
            }, error => {
                this._logger.error(JSON.stringify(error));
            });
        } else {
            this.listings = Array();
        }
    }

    /**
     * Shows up the information about listing, in browse mode
     *
     * @param listing listing clicked by user
     * @pre-cond    listing is not null
     */
    selectListing(listing:Listing){
        assert(listing, "listing can not be null");

        this.navCtrl.push(DetailPage,{
            data:this.listings,
            cursor:this.listings.indexOf(listing)
        });
        this._logger.debug("Listing " + this.listings.indexOf(listing) + " was clicked");
    }

    /**
     * Remove a listing from the user's favourites
     *
     * @param listing: listing to unfavourited
     * @pre-cond    listing is not null
     */
    unfavourite(listing: Listing) {
        assert(listing, "listing can not be null");

        let selectedIndex = this.listings.indexOf(listing);
        this.listings.splice(selectedIndex, 1);

        this.listingProvider.dislikeListing(listing.listingId).subscribe(data => {
            // Listing was removed
        }, error => {
            this.listingProvider.kasperService.handleError("likeDislikeListing", error.json());
        });
    }
}
