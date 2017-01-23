import {NgModule, ErrorHandler} from '@angular/core';
import {IonicApp, IonicModule, IonicErrorHandler} from 'ionic-angular';
import {MyApp} from './app.component';

import {SignInPage} from '../pages/sign-in/sign-in';
import {SignUpPage} from '../pages/sign-up/sign-up';
import {MainPage} from '../pages/main/main';
import {MyListingsPage} from "../pages/my-listings/my-listings";
import {SettingsPage} from "../pages/settings/settings";
import {TabsPage} from "../pages/tabs/tabs";

@NgModule({
    declarations: [
        MyApp,
        SignInPage,
        SignUpPage,
        MainPage,
        MyListingsPage,
        SettingsPage,
        TabsPage
    ],
    imports: [
        IonicModule.forRoot(MyApp, {tabsPlacement: 'bottom'})
    ],
    bootstrap: [IonicApp],
    entryComponents: [
        MyApp,
        SignInPage,
        SignUpPage,
        MainPage,
        MyListingsPage,
        SettingsPage,
        TabsPage
    ],
    providers: [{provide: ErrorHandler, useClass: IonicErrorHandler}]
})
export class AppModule {
}

