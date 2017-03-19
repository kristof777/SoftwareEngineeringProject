import {User} from "../../app/models/user";
import {ChangePasswordPage} from "../change-password/change-password";
import {Component} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {Province} from "../../app/models/province";
import {NavController, ModalController, Platform, AlertController} from "ionic-angular";
import {FormGroup, FormBuilder, Validators} from "@angular/forms";
import {LoginService} from "../../app/providers/login-service";
import {SignInPage} from "../sign-in/sign-in";
import {KasperService} from "../../app/providers/kasper-service";
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
                public alertCtrl: AlertController,
                public kasperService: KasperService,
                public loginService: LoginService,
                public platform: Platform,
                private _logger: Logger) {
        this.loadUser();

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

    /**
     * Set the user object for this page to display
     */
    loadUser(): void{
        assert(LoginService.user, "Tried to load a user but no user was logged in.");

        this.currentUser = LoginService.user;
    }

    /**
     * Display the dialog for the user to update their password.
     *
     * @post-cond   if data is returned, send the request to change the password.
     */
    showChangePassword(): void{
        let changePasswordModal = this.modalCtrl.create(ChangePasswordPage);

        changePasswordModal.onDidDismiss(data => {
            this._logger.debug("Password change was submitted");
            // If the user saves the change
            if(data) {
                this.updatePassword(data.oldPassword, data.newPassword, data.confirmPassword);
            }
        });

        changePasswordModal.present();
    }

    /**
     * Attempt to update the users password in the database.
     *
     * @param currentPassword   users input for their current password
     * @param newPassword       the new password
     * @param confirmedPassword the new password confirmed
     *
     * @pre-cond    no parameters are null
     */
    updatePassword(currentPassword: string, newPassword: string, confirmedPassword: string): void{
        assert(currentPassword, "currentPassword can not be null");
        assert(newPassword, "newPassword can not be null");
        assert(confirmedPassword, "confirmedPassword can not be null");

        let me = this;
        this._logger.debug("Verifying and changing password");

        this.kasperService.changePassword(currentPassword, newPassword, confirmedPassword).subscribe(data => {
            this.alertCtrl.create({
                title: "Success",
                subTitle: "Your password has been changed",
                buttons: ['Dismiss']
            }).present();

            me.loginService.setToken(data.authToken);
        }, error => {
            this.kasperService.handleError("changePassword", error.json());
        });
    }

    /**
     * Update the users information according to their input
     *
     * TODO updateUser
     */
    saveChanges(): void {
        this._logger.debug("Save button was clicked.");
    }

    /**
     * Sign the user out of this device.
     *
     * TODO signOut
     */
    signOut(): void{
        this._logger.debug("Sign-out was clicked.");
    }
}
