import {NgModule, ErrorHandler} from '@angular/core';
import {IonicApp, IonicModule, IonicErrorHandler} from 'ionic-angular';
import {Logger} from 'angular2-logger';
import {LOG_LOGGER_PROVIDERS} from "angular2-logger/core";
import {MyApp} from './app.component';

import {SignInPage} from '../pages/sign-in/sign-in';
import {SignUpPage} from '../pages/sign-up/sign-up';

import {MainPage} from '../pages/main/main';
import {DetailPage} from '../pages/detail/detail';
import {BrowsePage} from '../pages/browse/browse';
import {MyListingsPage} from '../pages/my-listings/my-listings';
import {FavouritesPage} from '../pages/favourites/favourites';
import {MyProfilePage} from '../pages/my-profile/my-profile';

import {EditListingsPage} from '../pages/edit-listings/edit-listings';
import {AddListingPage} from '../pages/add-listing/add-listing';

import {FilterPage} from '../pages/filter/filter';
import {ChangePasswordPage} from '../pages/change-password/change-password';
import {SavedListingProvider} from "./providers/saved-listing-provider";

@NgModule({
    declarations: [
        MyApp,
        SignInPage,
        SignUpPage,
        AddListingPage,
        EditListingsPage,
        FavouritesPage,
        FilterPage,
        ChangePasswordPage,
        MainPage,
        MyListingsPage,
        MyProfilePage,
        DetailPage,
        BrowsePage
    ],
    imports: [
        IonicModule.forRoot(MyApp, {tabsPlacement: 'bottom'})
    ],
    bootstrap: [IonicApp],
    entryComponents: [
        MyApp,
        SignInPage,
        SignUpPage,
        AddListingPage,
        EditListingsPage,
        FavouritesPage,
        FilterPage,
        ChangePasswordPage,
        MainPage,
        MyListingsPage,
        MyProfilePage,
        DetailPage,
        BrowsePage
    ],
    providers: [
        {provide: ErrorHandler, useClass: IonicErrorHandler},
        SavedListingProvider,
        Logger,
        LOG_LOGGER_PROVIDERS]
})
export class AppModule {
}

