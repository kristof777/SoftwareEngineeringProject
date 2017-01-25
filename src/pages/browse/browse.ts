let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavController, ToastController, ModalController, NavParams} from 'ionic-angular';

import {ListingModel} from '../../app/models/listing';
import {FilterPage} from '../filter/filter';

@Component({
    selector: 'page-browse',
    templateUrl: 'browse.html'
})
export class BrowsePage {
    // Fake listing data using. This structure will change
    data: ListingModel[] = [
        new ListingModel(
            1, // Listing ID
            1, // Lister ID
            "Saskatoon, SK", // Location
            "XXX Sask Place", // Address
            3, // Bedrooms
            4, // Bathrooms
            1800, // Square Feet
            288000, // Price
            // Description
            "Curabitur nec lacus diam. Maecenas placerat metus egestas sollicitudin malesuada. Mauris semper vehicula metus. Quisque faucibus nisl nec eros mollis, sit amet vulputate metus vehicula. Suspendisse non suscipit lorem. Ut metus magna, sollicitudin vitae facilisis vel, facilisis vel tellus. Donec bibendum pretium mauris. Praesent facilisis risus ut est accumsan imperdiet.",
            false, // isHidden
            "2017-01-01", // Date Created
            "2017-01-20", // Date Modified
            ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081","http://placehold.it/1920x1082","http://placehold.it/1920x1082","http://placehold.it/1920x1082"]
        ),
        new ListingModel(
            2,
            1,
            "Regina, SK",
            "123 Regina St.",
            2,
            2,
            1400,
            248000,
            "Cras vel porttitor orci. Sed eget efficitur sapien, in commodo felis. Etiam ac erat tincidunt, pellentesque ante ut, convallis purus. In ullamcorper mi at fermentum interdum. Proin id orci enim. Sed pharetra turpis ligula, non lacinia ipsum aliquet lacinia. Sed urna risus, pharetra in dui ut, vulputate tincidunt dui.",
            false,
            "2017-01-08",
            "2017-01-17",
            ["http://placehold.it/1280x720", "http://placehold.it/1280x721","http://placehold.it/1280x720"]
        )
    ];

    cursor: number = 0;

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                public modalCtrl: ModalController) {

        console.log("Array SIze: " + this.data.length);
    }

    goToFavourites(){
        console.log("Favourites was clicked");
    }

    goToFilters(){
        console.log("Filters was clicked");
        let filterModal = this.modalCtrl.create(FilterPage, { someData: "data" });

        filterModal.onDidDismiss(data => {
            console.log(data);
        });

        filterModal.present();
    }

    unlike(){
        console.log("Unlike was clicked");
    }

    like(){
        console.log("Like was clicked.");
    }

    nextProperty(){
        console.log("Next Property was clicked");
        if(this.cursor < (this.data.length - 1))
            this.cursor += 1;
    }

    previousProperty(){
        console.log("Previous Property was clicked");
        if(this.cursor > 0)
            this.cursor -= 1;
    }
}
