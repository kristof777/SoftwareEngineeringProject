import {NgModule, ErrorHandler} from '@angular/core';
import {IonicApp, IonicModule, IonicErrorHandler} from 'ionic-angular';
import {MyApp} from './app.component';

import {SignInPage} from '../pages/sign-in/sign-in'
import {SignUpPage} from '../pages/sign-up/sign-up';
import {EditListingsPage} from '../pages/edit-listings/edit-listings';
import {FavouritesPage} from '../pages/favourites/favourites';
import {FavouritesListPage} from '../pages/favourites-list/favourites-list';
import {AddListingPage} from '../pages/add-listing/add-listing';
import {FilterPage} from '../pages/filter/filter';
import {MainPage} from '../pages/main/main';
import {MyListingsPage} from '../pages/my-listings/my-listings';
import {SettingsPage} from '../pages/settings/settings';



@NgModule({
    declarations: [
        MyApp,
        SignInPage,
        SignUpPage,
        AddListingPage,
        EditListingsPage,
        FavouritesPage,
        FavouritesListPage,
        FilterPage,
        MainPage,
        MyListingsPage,
        SettingsPage

    ],
    imports: [
        IonicModule.forRoot(MyApp)
    ],
    bootstrap: [IonicApp],
    entryComponents: [
        MyApp,
        SignInPage,
        SignUpPage,
        AddListingPage,
        EditListingsPage,
        FavouritesPage,
        FavouritesListPage,
        FilterPage,
        MainPage,
        MyListingsPage,
        SettingsPage

    ],
    providers: [{provide: ErrorHandler, useClass: IonicErrorHandler}]
})
export class AppModule {
}
