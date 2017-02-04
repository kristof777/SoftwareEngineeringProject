import {NgModule, ErrorHandler} from '@angular/core';
import {IonicApp, IonicModule, IonicErrorHandler} from 'ionic-angular';
import {Logger} from 'angular2-logger';
import {LOG_LOGGER_PROVIDERS} from "angular2-logger/core";
import {MyApp} from './app.component';

import {SignInPage} from '../pages/sign-in/sign-in';
import {SignUpPage} from '../pages/sign-up/sign-up';

import {MainPage} from '../pages/main/main';
import {BrowsePage} from '../pages/browse/browse';
import {MyListingsPage} from '../pages/my-listings/my-listings';
import {SettingsPage} from '../pages/settings/settings';

import {EditListingsPage} from '../pages/edit-listings/edit-listings';
import {AddListingPage} from '../pages/add-listing/add-listing';

import {FilterPage} from '../pages/filter/filter';
import {ChangePasswordPage} from '../pages/change-password/change-password';

@NgModule({
    declarations: [
        MyApp,
        SignInPage,
        SignUpPage,
        AddListingPage,
        EditListingsPage,
        FilterPage,
        ChangePasswordPage,
        MainPage,
        MyListingsPage,
        SettingsPage,
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
        FilterPage,
        ChangePasswordPage,
        MainPage,
        MyListingsPage,
        SettingsPage,
        BrowsePage
    ],
    providers: [{provide: ErrorHandler, useClass: IonicErrorHandler}, Logger, LOG_LOGGER_PROVIDERS]
})
export class AppModule {
}

