let assert = require('assert-plus');
import {ExampleTest} from "../example.test";
import {Component} from '@angular/core';
import {Logger} from "angular2-logger/core";
import {NavController} from 'ionic-angular';

@Component({
    selector: 'page-run-test',
    templateUrl: 'run-test.html',
    providers: [ExampleTest]
})
export class RunTestPage {

    /**
     * Import and add the injectable class into the constructor of this class, and call the
     * method in the constructor.
     */
    constructor(public navCtrl: NavController,
                public exampleTest: ExampleTest, // This is the injectable test
                private _logger: Logger) {

        // execute the run() functions of the test files.
        exampleTest.run();
    }
}
