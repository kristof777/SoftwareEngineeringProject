import {ListingProvider} from "../../app/providers/listing-provider";
import {Component} from "@angular/core";
import {NavController} from "ionic-angular";
import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');

@Component({
    selector: 'page-browse',
    templateUrl: 'browse.html',
    providers: [ListingProvider]
})
export class BrowsePage {
    constructor(public navCtrl: NavController,
                private _logger: Logger,) {
    }

}
