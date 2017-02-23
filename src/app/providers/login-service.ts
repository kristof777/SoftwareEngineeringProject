import { Injectable } from '@angular/core';
import 'rxjs/add/operator/map';
import {Logger} from "angular2-logger/core";
import {User} from "../models/user";
let assert = require('assert-plus');

@Injectable()
export class LoginService {
    user: User;

    constructor(private _logger: Logger) {
    }

}
