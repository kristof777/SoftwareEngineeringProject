import {Logger} from "angular2-logger/core";
let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavParams} from 'ionic-angular';

@Component({
    selector: 'page-filter',
    templateUrl: 'filter.html'
})
export class FilterPage {

    constructor(params: NavParams,
                private _logger: Logger) {
        this._logger.debug("Filter created");
    }

}
