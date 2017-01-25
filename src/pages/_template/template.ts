let assert = require('assert-plus');
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";

import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-template',
    templateUrl: 'template.html'
})
export class TemplatePage {

    constructor(public navCtrl: NavController,
                private _logger: Logger) {

    }
}
