import {LoginService} from "../../app/providers/login-service";
import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from "@angular/core";
import {NavController, ModalController} from "ionic-angular";
import {Listing} from "../../app/models/listing";
import {Logger} from "angular2-logger/core";
import {DetailPage} from "../detail/detail";
import {AddListingPage} from "../add-listing/add-listing";
let assert = require('assert-plus');

@Component({
    selector: 'page-my-listings',
    templateUrl: 'my-listings.html',
    providers: [ListingProvider]

})
export class MyListingsPage {
    listings: Listing[];

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                public listingProvider: ListingProvider,
                public loginService: LoginService,
                private _logger: Logger) {

        this.listings = Array();
    }
   //Documentation for this please in diff file 
    ionViewDidEnter(){
        let me = this;

        if(this.loginService.isLoggedIn()) {
            this.listingProvider.getMyListings().subscribe(data => {
                me.listings = data['listings'];
            }, error => {
                this._logger.error(JSON.stringify(error));
            });
        }
    }
//add precondition & assert \/ 
    /**
     * Display the detailed view for the selected listing
     *
     * @param listing listing clicked by user
     */
    selectListing(listing:Listing){
        this.navCtrl.push(DetailPage, {
            data: this.listings,
            cursor: this.listings.indexOf(listing)
        });
        this._logger.debug("Listing  " + listing + " was clicked") //probably changed to listing id and semicolon
    }
    //precondition that listing is null \/
    /**
     * Display the edit listing view for the selected listing
     *
     * @param listing: listing to be edited
     */
    editListing(listing:Listing){ //add asserts to methods
        this.navCtrl.push(AddListingPage,{ //add comment to explain that addListingPage is the same as edit...
            listing:listing
        });
        this._logger.debug("Trying to edit...") //a better explaination  for debug

    }//semicolon
//pre condition assert logging
    /**
     * fixx me
     * @param listing: listing to be deleted
     */
    deleteListing(listing:Listing){
        let selectedIndex = this.listings.indexOf(listing);
        this.listings.splice(selectedIndex, 1);
    }

    /**
     * Takes you to listing page
     */
    addListing(){

        this.navCtrl.push(AddListingPage);
        //gimme a log
    }

    /**
     * Get the Unpublished listing
     *
     * @returns {Listing[]}  Unpublished listing
     */
    getUnpublished(): Listing[]{
        let result: Listing[] = [];

        for(let i=0; i<this.listings.length; i++){
            if(!this.listings[i].isPublished)
                result.push(this.listings[i]);
        }

        return result;
    }

    /**
     * Get the published listing
     *
     * @returns {Listing[]}  Published listing
     */
    getPublished(): Listing[]{
        let result: Listing[] = [];

        for(let i=0; i<this.listings.length; i++){
            if(this.listings[i].isPublished)
                result.push(this.listings[i]);
        }

        return result;
    }
}
