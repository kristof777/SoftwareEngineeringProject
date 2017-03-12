import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Component} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {
    NavController, ToastController, ViewController, LoadingController,
    Loading, AlertController
} from "ionic-angular";

import { Facebook, Toast } from 'ionic-native';
import {SignUpPage} from "../sign-up/sign-up";
import {KasperService} from "../../app/providers/kasper-service";
import {User} from "../../app/models/user";
import {Province} from "../../app/models/province";
import {MyProfilePage} from "../my-profile/my-profile";
let assert = require('assert-plus');

@Component({
    selector: 'page-sign-in',
    templateUrl: 'sign-in.html',
    providers: [KasperService]
})
export class SignInPage {
    FB_APP_ID: number = 623532211163253;
    loginForm: FormGroup;
    private emailAttempted: boolean = false;

    private loading: Loading;

    constructor(public navCtrl: NavController,
                public alertCtrl: AlertController,
                private _logger: Logger,
                public loadingCtrl: LoadingController,
                public formBuilder: FormBuilder,
                public kasperService: KasperService) {
        Facebook.browserInit(this.FB_APP_ID, "v2.8");
        console.log("initialized");
        this.loginForm = formBuilder.group({
            email: ['', Validators.compose([Validators.pattern("^(.+)@(.+){2,}\.(.+){2,}"), Validators.required])],
            password: ['', Validators.compose([Validators.required])],
        });
    }

    /**
     * Switch the user to the navigation screen.
     */
    pushRegister(): void{
        this._logger.debug("Register was clicked.");
        // This variable is injected through the constructor.
        this.navCtrl.push(SignUpPage);
    }

    // TODO make this function block
    /**
     * Attempt to log the user in with the provided information
     */
    doSignIn(): void{
        this._logger.debug("Sign In was clicked.");

        if(this.loginForm.value.email == "test") {
            let userID: number = 1;
            let email: string = "john.doe@gmail.com";
            let firstName: string = "John";
            let lastName: string = "Doe";
            let phone1: string = "3065555555";
            let phone2: string = null;
            let province = Province.SK;
            let city = "Saskatoon";

            let testUser = new User(userID, email, firstName, lastName, phone1, phone2, province, city);

            this.kasperService.loginService.setUser(testUser);

            this.navCtrl.setRoot(MyProfilePage);
        } else if(this.loginForm.valid){
            let test = this.kasperService.login(this.loginForm.value.email, this.loginForm.value.password);

            this.loading = this.loadingCtrl.create({
                content: "Logging in..."
            });
            this.loading.present();

            this.signInCallback(test);
        } else {
            this._logger.error("Tried to submit when fields do not pass validation.");
        }
    }

    facebookLogin(): void{
        let permissions = new Array();
        let nav = this.navCtrl;
    //the permissions your facebook app needs from the user
    permissions = ["public_profile", "email"];
    Facebook.login(permissions)
    .then(function(response){
      let userId = response.authResponse.userID;
      let params = new Array();

      //Getting name and gender properties
      Facebook.api("/me?fields=first_name,last_name,email", params)
      .then(function(user) {
          console.log("Printing user stuff");
          console.log(user);
          console.log(userId);
          console.log(user.name);
          console.log(user.gender);

      })
    }, function(error){
        Toast.show("I'm a good toast", '5000', 'center');
        console.log(error);
    });
    }

    /**
     * Handle data from the login request
     *
     * @param result the response from the server
     */
    signInCallback(result: any): void{
        result.subscribe(data => {
            // Create a user object from the result of the login statement
            let user: User = new User(data.userId, data.email, data.firstName, data.lastName,
                data.phone1, data.phone2, Province.fromAbbr(data.province), data.city);

            // Set the login data for the user
            this.kasperService.loginService.setUser(user);
            this.kasperService.loginService.setToken(data.token);

            // Set the root of the current tab to the MyProfile page.
            this.navCtrl.setRoot(MyProfilePage);

            // Move back to the browse page.
            // This is currently required as selecting the My Profile tab a second time (before
            // changing to another tab) will bring the user back to the SignInPage page.
            this.navCtrl.parent.select(0);

            }, error => {
                this._logger.error("signIn error: " + JSON.stringify(error));
                this.kasperService.handleError(error.json());
            });
        this.loading.dismiss();
    }

    attemptEmail(){
        this.emailAttempted = true;
    }
}
