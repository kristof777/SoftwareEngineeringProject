import {Component} from '@angular/core';
import {Platform} from 'ionic-angular';
import {StatusBar, Splashscreen, SQLite} from 'ionic-native';

import {SignInPage} from '../pages/sign-in/sign-in';
import {KasperConfig} from "./kasper-config";
import {Logger} from "angular2-logger/core";

@Component({
    templateUrl: 'app.html'
})
export class MyApp {
    rootPage = SignInPage;

    constructor(platform: Platform,
                private _logger: Logger) {
        platform.ready().then(() => {
            // Okay, so the platform is ready and our plugins are available.
            // Here you can do any higher level native things you might need.
            StatusBar.styleDefault();
            Splashscreen.hide();

            let db = new SQLite();
            db.openDatabase(KasperConfig.DB_INFO).then(() => {
                this.createLoginTable(db);
            }, error => {
                this._logger.error("Could not access SQLite database: ");
                this._logger.error(error);
            });
        });
    }

    /**
     * Creates the table containing the user's session info.
     *
     * @param db  an open SQLite connection
     */
    private createLoginTable(db: SQLite): void {
        db.executeSql(
            "CREATE TABLE IF NOT EXISTS session(" +
            "userId       INT PRIMARY KEY, " +
            "token        VARCHAR(255), " +
            "created_date DATETIME)", {})
            .then(() => {
                // Don't do anything if it's created successfully or already exists.
            }, error => {
                this._logger.error("Could not create session table: ");
                this._logger.error(error);
            });
    }

    /**
     * Creates the table containing the listings and another containing the
     * images for the listings
     *
     * @param db  an open SQLite connection
     */
    private createListingTables(db: SQLite): void {
        db.executeSql(
            "CREATE TABLE IF NOT EXISTS listings ( " +
            "listingId    INT PRIMARY KEY, " +
            "listerId     INT, " +
            "bedrooms     INT, " +
            "bathrooms    INT, " +
            "squarefeet   INT, " +
            "price        INT, " +
            "description  TEXT, " +
            "isPublished  BOOLEAN, " +
            "createdDate  DATE, " +
            "modifiedDate DATE, " +
            // Location data
            "province     TEXT, " +
            "city         TEXT, " +
            "address      TEXT, " +
            "postalCode   TEXT, " +
            "longitude    REAL, " +
            "latitude     REAL);", {})
            .then(() => {
            // Don't do anything if it's created successfully or already exists.
        }, (error) => {
            this._logger.error("Could not create listings table: ");
            this._logger.error(error);
        });

        db.executeSql(
            "CREATE TABLE IF NOT EXISTS listing_images ( " +
            "listingId INT PRIMARY KEY, " +
            "sortOrder INT, " +
            "data      TEXT);", {})
            .then(() => {
                // Don't do anything if it's created successfully or already exists.
            }, (error) => {
                this._logger.error("Could not create listings_images table: ");
                this._logger.error(error);
        });
    }
}
