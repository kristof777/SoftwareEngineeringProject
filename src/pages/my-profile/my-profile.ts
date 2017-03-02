import {User} from "../../app/models/user";
import {ChangePasswordPage} from "../change-password/change-password";
import {Component} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {Province} from "../../app/models/province";
import {NavController, ModalController, Platform} from "ionic-angular";
import {FormGroup, FormBuilder, Validators} from "@angular/forms";
import {LoginService} from "../../app/providers/login-service";
import {SignInPage} from "../sign-in/sign-in";
let assert = require('assert-plus');

@Component({
    selector: 'page-my-profile',
    templateUrl: 'my-profile.html'
})
export class MyProfilePage {
    private provinces: Province[];

    profileGroup: FormGroup;

    currentUser: User;

    email: string;
    firstName: string;
    lastName: string;
    phone1: string;
    phone2: string;
    province: string;
    city: string;

    constructor(public navCtrl: NavController,
                public modalCtrl: ModalController,
                public formBuilder: FormBuilder,
                public loginService: LoginService,
                public platform: Platform,
                private _logger: Logger) {
        if(!this.loginService.isLoggedIn()){
            navCtrl.setRoot(SignInPage);
        } else {
            this.loadUser();
        }

        this.provinces = Province.asArray;

        this.profileGroup = this.formBuilder.group({
            email: [null, Validators.compose([Validators.pattern("^(.+)@(.+){2,}\.(.+){2,}")])],
            firstName: [null, Validators.compose([])],
            lastName: [null, Validators.compose([])],
            phone1: [null, Validators.compose([])],
            phone2: [null, Validators.compose([])],
            province: [null, Validators.compose([])],
            city: [null, Validators.compose([])],
            notificationsEnabled: [null, Validators.compose([])],
        });
    }

    loadUser(): void{
        assert.object(LoginService.user, "Tried to load a user but no user was logged in.");

        this.currentUser = LoginService.user;
    }

    /**
     * Display the dialog for the user to update their password.
     */
    showChangePassword(): void{
        let changePasswordModal = this.modalCtrl.create(ChangePasswordPage);

        changePasswordModal.onDidDismiss(data => {
            this._logger.debug("Password change was submitted");
            // If the user saves the change
            if(data) {
                this.updatePassword(data.oldPassword, data.newPassword);
            }
        });

        changePasswordModal.present();
    }

    /**
     * Attempt to update the users password in the database.
     *
     * @param currentPassword   users input for their current password
     * @param newPassword       the new password
     */
    updatePassword(currentPassword: string, newPassword: string): void{
        // Need to verify currentPassword is correct
        // newPassword has already been checked for strength.
        this._logger.debug("Verifying and changing password");
    }

    /**
     * Update the users information according to their input
     */
    saveChanges(): void {
        this._logger.debug("Save button was clicked.");
    }

    /**
     * Sign the user out of this device.
     */
    signOut(): void{
        this._logger.debug("Sign-out was clicked.");
    }
}
