let assert = require('assert-plus');
import {Component} from '@angular/core';

import {NavParams} from 'ionic-angular';

@Component({
    selector: 'page-filter',
    templateUrl: 'filter.html'
})
export class FilterPage {

    constructor(params: NavParams) {
        console.log("Filter created");
    }

}
