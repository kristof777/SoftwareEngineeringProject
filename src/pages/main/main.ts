import { Component } from '@angular/core';

import {MyProfilePage} from "../my-profile/my-profile";
import {MyListingsPage} from "../my-listings/my-listings";
import {BrowsePage} from "../browse/browse";
import {FavouritesPage} from "../favourites/favourites";

@Component({
    templateUrl: '../main/main.html'
})
export class MainPage {
    tab1Root: any = BrowsePage;
    tab2Root: any = MyListingsPage;
    tab3Root: any = FavouritesPage;
    tab4Root: any = MyProfilePage;

    constructor() {}
}
