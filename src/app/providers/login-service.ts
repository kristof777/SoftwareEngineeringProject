let assert = require('assert-plus');
import {KasperConfig} from "../kasper-config";
import {Injectable} from "@angular/core";
import {SQLite} from "ionic-native";
import "rxjs/add/operator/map";
import {Logger} from "angular2-logger/core";
import {User} from "../models/user";
import {Platform} from "ionic-angular";

/**
 * LoginService holds the current session data of a user, and saves the session data to the device
 * for the app to automatically sign to sign in with later.
 */
@Injectable()
export class LoginService {
    private db: SQLite;

    // The data previously stored in the database
    private userId: number;
    private token: string;

    // The user object returned after logging in
    public static user: User;

    constructor(private _logger: Logger,
                private platform: Platform) {
        this.platform.ready().then(() => {
            this.db = new SQLite();

            this.db.openDatabase(KasperConfig.DB_INFO)
                .then(() => {
                    this.loadSessionInfo();
                }, error => {
                    this._logger.error("Could not access database: ");
                    this._logger.error(JSON.stringify(error));
                });
        });
    }

    /**
     * Set the logged in user
     *
     * @param user   the user who is logged in
     */
    public setUser(user: User){
        LoginService.user = user;
        this.userId = user.id;
    }

    /**
     * Update the token for the currently logged in user.
     *
     * @param token the new token
     */
    public setToken(token: string): void{
        assert.string(token, "The received token was not a string");

        this.token = token;
        this.updateToken(token);

        this._logger.debug("New token has been set: " + token);
    }

    /**
     * Get the currently logged in user's id
     *
     * @returns {number}    the id
     */
    public getUserId(): number{
        assert.number(this.userId, "The userId is not defined");

        return this.userId;
    }

    /**
     * Get the currently stored token
     * @returns {string}    the token
     */
    public getToken(): string{
        assert.string(this.token, "The token is not defined");

        return this.token;
    }

    /**
     * Insert a new userId/token pair into the users.
     *
     * @param token the token to insert
     */
    private updateToken(token: string){
        assert.object(LoginService.user, "A user must be logged in to update the token.");
        assert.object(this.db, "A database connection was not established.");

        this.db.executeSql("INSERT INTO session (userId, token, created_date) VALUES (?, ?, datetime(now))", [
            this.userId, this.token]).then(() => {
            this._logger.debug("New session token was saved successfully.");
        }, error => {
            this._logger.error("Could not insert new session token: ");
            this._logger.error(JSON.stringify(error));
        });
    }

    /**
     * Load the most recent userId and token from the users phone.
     */
    private loadSessionInfo(){
        assert.object(LoginService.user, "A user must be logged in to update the token.");
        assert.object(this.db, "A database connection was not established.");

        this.db.executeSql("SELECT userId, token FROM session ORDER BY created_date DESC LIMIT 1", {}).then((data) => {
            if(!data.rows) {
                this.userId = data.rows.item(0).userId;
                this.token = data.rows.item(0).token;
                this._logger.debug(`Loaded previous session info: {userId: ${this.userId}, token: ${this.token}`);
            } else {
                this._logger.debug("There was no login session stored on the device");
            }
        }, error => {
            this._logger.error("Error selecting session from SQLite database: ");
            this._logger.error(JSON.stringify(error));
        });
    }

    /**
     * Checks whether a user is currently set.
     *
     * @returns {boolean} true if the user is logged in
     */
    public isLoggedIn(): boolean{
        return !!LoginService.user;
    }
}
