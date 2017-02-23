let assert = require('assert-plus');
import {KasperConfig} from "../kasper-config";
import { Injectable } from '@angular/core';
import {SQLite} from "ionic-native"
import 'rxjs/add/operator/map';
import {Logger} from "angular2-logger/core";
import {User} from "../models/user";
import {Platform} from "ionic-angular";

@Injectable()
export class LoginService {
    private db: SQLite;

    // The data previously stored in the database
    private userId: number;
    private token: string;

    // The user object returned after logging in
    private static user: User;

    constructor(private _logger: Logger,
                private platform: Platform) {
        this.platform.ready().then(() => {
            this.db = new SQLite();

            this.db.openDatabase(KasperConfig.DB_INFO)
                .then(() => {
                    this.loadSessionInfo();
                }, error => {
                    this._logger.error("Could not access database: ");
                    this._logger.error(error);
                });
        });
    }

    public setUser(user: User){
        LoginService.user = user;
        this.userId = user.id;
    }

    public setToken(token: string): void{
        this.token = token;
        this.updateToken(token);
        this._logger.info("New token has been set: " + token);
    }

    public getUserId(): number{
        return this.userId;
    }

    public getToken(): string{
        return this.token;
    }

    private updateToken(token: string){
        this.db.executeSql("INSERT INTO session (userId, token, created_date) VALUES (?, ?, datetime(now))", [
            this.userId, this.token]).then(() => {
            this._logger.info("New session token was saved successfully.");
        }, error => {
            this._logger.error("Could not insert new session token: ");
            this._logger.error(error);
        });
    }

    private loadSessionInfo(){
        this.db.executeSql("SELECT userId, token FROM session ORDER BY created_date DESC LIMIT 1", {}).then((data) => {
            if(!data.rows) {
                this.userId = data.rows.item(0).userId;
                this.token = data.rows.item(0).token;
                this._logger.info(`Loaded previous session info: {userId: ${this.userId}, token: ${this.token}`);
            } else {
                this._logger.info("There was no login session stored on the device");
            }
        }, error => {
            this._logger.error("Error selecting session from SQLite database: ");
            this._logger.error(error);
        });


    }
}
