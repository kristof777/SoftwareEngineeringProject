import {Component, ViewChild} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {NavController, ToastController, Slides, Platform} from "ionic-angular";
import {KasperService} from "../../app/providers/kasper-service";
import {MainPage} from "../main/main";
import {FormGroup, FormBuilder, Validators} from "@angular/forms";
let assert = require('assert-plus');

@Component({
    selector: 'page-sign-up',
    templateUrl: 'sign-up.html',
    providers: [KasperService]
})
export class SignUpPage {
    @ViewChild(Slides) slides: Slides;
    selectedMode: number;

    // Form validation
    signUpStep1: FormGroup;
    private emailAttempted: boolean = false;
    private passwordAttempted: boolean = false;
    private confirmPasswordAttempted: boolean = false;

    signUpStep2: FormGroup;
    private firstNameAttempted: boolean = false;

    signUpStep3: FormGroup;

    constructor(public navCtrl: NavController,
                private _logger: Logger,
                public formBuilder: FormBuilder,
                public toastCtrl: ToastController,
                public kasperService: KasperService,
                public platform: Platform) {

        // Create validation for step 1
        this.signUpStep1 = formBuilder.group({
            email: [null, Validators.compose([Validators.required,
                Validators.pattern("^(.+)@(.+){2,}\.(.+){2,}")])],
            password: [null, Validators.compose([Validators.required, kasperService.checkPass])],
            confirmPassword: [null, Validators.compose([Validators.required])],
        });

        // Create validation for step 2
        this.signUpStep2 = formBuilder.group({
            firstName: [null, Validators.compose([Validators.required])],
            lastName: ['', Validators.compose([])],
            // TODO validate phoneNumber
            phoneNumber: ['', Validators.compose([kasperService.checkPhone])],
        });

        // Create validation for step 3
        this.signUpStep3 = formBuilder.group({
            province: ['', Validators.compose([Validators.required])],
            city: ['', Validators.compose([])],
        });

        // Disable swiping (has to be done after page load)
        platform.ready().then(() => {
            this.slides.lockSwipes(true);
        });
    }

    doRegister(): void{
        this.kasperService.signUp(this.signUpStep1.value.email,
                                this.signUpStep1.value.password,
                                this.signUpStep1.value.confirmPassword,
                                this.signUpStep2.value.firstName,
                                this.signUpStep2.value.lastName,
                                this.signUpStep3.value.phoneNumber,
                                "", // phone2
                                this.signUpStep3.value.city,
                                this.signUpStep3.value.province,
                                this.registerCallback);
        this.navCtrl.setRoot(MainPage);
    }

    registerCallback(data: JSON){

    }

    /**
     * Go to the next step if the fields are valid
     */
    nextStep(): void{
        if(this.confirmStep()){
            if(this.slides.getActiveIndex() != 2) {
                this.slides.lockSwipes(false);
                this.slides.slideTo(this.slides.getActiveIndex() + 1);
                this.slides.lockSwipes(true);
            } else {
                this.doRegister();
            }
        } else {
            this.attemptAll();
            this.toastCtrl.create({
                message: "Please validate fields before continuing.",
                duration: 3000,
                position: 'top'
            }).present();
        }
    }

    previousStep(): void{
        if(this.slides.getActiveIndex() != 0) {
            this.slides.lockSwipes(false);
            this.slides.slideTo(this.slides.getActiveIndex() - 1);
            this.slides.lockSwipes(true);
        }
    }

    /**
     * Confirm the validity of the current step
     *
     * @returns {boolean}   true if the fields are valid
     *                      false otherwise
     */
    confirmStep(): boolean {
        switch (this.slides.getActiveIndex()) {
            case 0:
                return (this.signUpStep1.valid &&
                this.signUpStep1.value.password == this.signUpStep1.value.confirmPassword);
            case 1:
                return this.signUpStep2.valid;
            case 2:
                return this.signUpStep3.valid;
        }
    }

    /////////////////////////////
    // Form Validation Helpers

    attemptAll(){
        if(this.slides.getActiveIndex() == 0) {
            this.attemptEmail();
            this.attemptPassword();
            this.attemptConfirmPassword();
        } else if (this.slides.getActiveIndex() == 1){
            this.attemptFirstName();
        } else if (this.slides.getActiveIndex() == 2){

        }
    }

    attemptEmail(){
        this.emailAttempted = true;
    }

    attemptPassword(){
        this.passwordAttempted = true;
    }

    attemptConfirmPassword(){
        this.confirmPasswordAttempted = true;
    }

    attemptFirstName(){
        this.firstNameAttempted = true;
    }
}
