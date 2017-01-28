import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavParams} from 'ionic-angular';

@Component({
    selector: 'page-filter',
    templateUrl: 'filter.html'
})
export class FilterPage {

    // ngModel binds the value of the html element to variable "province"
    // to access use this.province
    province: string;




    // Creates the logger object (needed in all constructors
    constructor(params: NavParams,
                private _logger: Logger) {
        this._logger.debug("Filter created");
    }

}
