import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Component} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {NavController, ToastController, ViewController} from "ionic-angular";
import {SignUpPage} from "../sign-up/sign-up";
import {KasperService} from "../../app/providers/kasper-service";
import {User} from "../../app/models/user";
import {Location} from "../../app/models/location";
import {Province} from "../../app/models/province";
import {MyProfilePage} from "../my-profile/my-profile";
let assert = require('assert-plus');

@Component({
    selector: 'page-sign-in',
    templateUrl: 'sign-in.html',
    providers: [KasperService]
})
export class SignInPage {
    loginForm: FormGroup;
    private emailAttempted: boolean = false;

    constructor(public navCtrl: NavController,
                public toastCtrl: ToastController,
                private _logger: Logger,
                public formBuilder: FormBuilder,
                public viewCtrl: ViewController,
                public kasperService: KasperService) {
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
            let location: Location = new Location(Province.SK, "Saskatoon", "1234 Saskatoon St.", "A1B2C3", 0.0, 0.0);

            let testUser = new User(userID, email, firstName, lastName, phone1, phone2, location);

            this.kasperService.loginService.setUser(testUser);

            this.navCtrl.setRoot(MyProfilePage);
        } else if(this.loginForm.valid){
            let test = this.kasperService.login(this.loginForm.value.email, this.loginForm.value.password);
            this.signInCallback(test);
        } else {
            this._logger.error("Tried to submit when fields do not pass validation.");
        }
    }

    facebookLogin(): void{}

    /**
     * Handle data from the login request
     *
     * @param result the response from the server
     */
    signInCallback(result: any): void{
        result.subscribe(data => {
            this.kasperService.loginService.setUser(
                new User(data.userId, data.email, data.firstName, data.lastName,  data.phone1, data.phone2,
                    new Location(Province.fromAbbr(data.province), data.city, "", "", 0.0, 0.0)
                ));
            this.kasperService.loginService.setToken(data.token);
            this.navCtrl.setRoot(MyProfilePage);
            }, error => {
                this._logger.error("Error ")
                this._logger.error(JSON.stringify(error));
            });
    }

    attemptEmail(){
        this.emailAttempted = true;
    }
}
