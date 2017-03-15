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
    private authToken: string;

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
     * Update the auth token for the currently logged in user.
     *
     * @param authToken the new token
     */
    public setToken(authToken: string): void{
        assert.string(authToken, "The received token was not a string");

        this.authToken = authToken;
        this.updateAuthToken(authToken);

        this._logger.debug("New auth token has been set: " + authToken);
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
     * Get the currently stored authtoken
     * @returns {string}    the auth token
     */
    public getAuthToken(): string{
        assert.string(this.authToken, "The token is not defined");

        return this.authToken;
    }

    /**
     * Insert a new userId/authToken pair into the users.
     *
     * @param authToken the token to insert
     */
    private updateAuthToken(authToken: string){
        assert.object(LoginService.user, "A user must be logged in to update the auth token.");
        assert.object(this.db, "A database connection was not established.");

        this.db.executeSql("INSERT INTO session (userId, authToken, created_date) VALUES (?, ?, datetime(now))", [
            this.userId, this.authToken]).then(() => {
            this._logger.debug("New session auth token was saved successfully.");
        }, error => {
            this._logger.error("Could not insert new session auth token: ");
            this._logger.error(JSON.stringify(error));
        });
    }

    /**
     * Load the most recent userId and auth token from the users phone.
     */
    private loadSessionInfo(){
        assert.object(LoginService.user, "A user must be logged in to update the auth token.");
        assert.object(this.db, "A database connection was not established.");

        this.db.executeSql("SELECT userId, authToken FROM session ORDER BY created_date DESC LIMIT 1", {}).then((data) => {
            if(!data.rows) {
                this.userId = data.rows.item(0).userId;
                this.authToken = data.rows.item(0).authToken;
                this._logger.debug(`Loaded previous session info: {userId: ${this.userId}, token: ${this.authToken}`);
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
