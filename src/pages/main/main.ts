import { Component } from '@angular/core';

import {SettingsPage} from "../settings/settings";
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
    tab4Root: any = SettingsPage;

    constructor() {
    }
}
