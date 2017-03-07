let assert = require('assert-plus');
import {Component} from "@angular/core";
import {Logger} from "angular2-logger/core";
import {NavController} from "ionic-angular";

@Component({
    selector: 'page-contact',
    templateUrl: 'contact.html'
})
export class ContactPage {

    constructor(public navCtrl: NavController,
                private _logger: Logger) {

    }

    sendMessage(){

    }
}
