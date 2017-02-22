let assert = require('assert-plus');
import {Injectable} from "@angular/core";
import "rxjs/add/operator/map";
import {Logger} from "angular2-logger/core";
import {Http} from "@angular/http";

@Injectable()
export class ExampleTest {

    constructor(public http: Http,
                private _logger: Logger) {
    }

    /**
     * Create a run() method in every test file that runs all the tests.
     */
    run(){
        this.testA();
        this.testB();
    }

    /**
     * Create descriptive methods and call them in the run method.
     */
    testA(){
        assert.equal(1, 1, "1 isn't 1");
    }

    testB(){
        assert.equal(1, 2, "1 isn't 2");
    }
}
