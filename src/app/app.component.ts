import {Component} from '@angular/core';
import {Platform} from 'ionic-angular';
import {StatusBar, Splashscreen} from 'ionic-native';

import {SignInPage} from '../pages/sign-in/sign-in';
import {MainPage} from "../pages/main/main";
import {TabsPage} from "../pages/tabs/tabs";


@Component({
    templateUrl: 'app.html'
})
export class MyApp {
    //rootPage = SignInPage;
    rootPage=TabsPage;

    constructor(platform: Platform) {
        platform.ready().then(() => {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            StatusBar.styleDefault();
            Splashscreen.hide();
        });
    }
}
