import { Component } from '@angular/core';

import {MyProfilePage} from "../my-profile/my-profile";
import {MyListingsPage} from "../my-listings/my-listings";
import {BrowsePage} from "../browse/browse";
import {FavouritesPage} from "../favourites/favourites";

@Component({
    template:
        `<ion-tabs color="primary">
            <ion-tab [root]="tab1Root" tabTitle="Browse" tabIcon="search"></ion-tab>
            <ion-tab [root]="tab2Root" tabTitle="Favourites" tabIcon="heart"></ion-tab>
            <ion-tab [root]="tab3Root" tabTitle="My Profile" tabIcon="person"></ion-tab>
            <ion-tab [root]="tab4Root" tabTitle="My Listings" tabIcon="list-box"></ion-tab>
        </ion-tabs>`
})
export class MainPage {
    tab1Root: any = BrowsePage;
    tab2Root: any = FavouritesPage;
    tab3Root: any = MyProfilePage;
    tab4Root: any = MyListingsPage;

    constructor() {}
}
