import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';
import {ListingModel} from "../models/listing";

@Injectable()
export class ListingProvider {
    data: any;

    constructor(public http: Http) {
        this.data = [
            new ListingModel(1, 1, "Saskatoon, SK", "XXX Sask Place", 3, 4, 1800, 288000, "Curabitur nec lacus diam. Maecenas placerat metus egestas sollicitudin malesuada. Mauris semper vehicula metus. Quisque faucibus nisl nec eros mollis, sit amet vulputate metus vehicula. Suspendisse non suscipit lorem. Ut metus magna, sollicitudin vitae facilisis vel, facilisis vel tellus. Donec bibendum pretium mauris. Praesent facilisis risus ut est accumsan imperdiet.", false, "2017-01-01","2017-01-20", ["http://placehold.it/1920x1080", "http://placehold.it/1920x1081","http://placehold.it/1920x1082","http://placehold.it/1920x1082","http://placehold.it/1920x1082"]),
            new ListingModel(2, 1, "Regina, SK", "123 Regina St.", 2, 2, 1400, 248000, "Cras vel porttitor orci. Sed eget efficitur sapien, in commodo felis. Etiam ac erat tincidunt, pellentesque ante ut, convallis purus. In ullamcorper mi at fermentum interdum. Proin id orci enim. Sed pharetra turpis ligula, non lacinia ipsum aliquet lacinia. Sed urna risus, pharetra in dui ut, vulputate tincidunt dui.", false, "2017-01-08", "2017-01-17", ["http://placehold.it/1280x720", "http://placehold.it/1280x721","http://placehold.it/1280x720"])
        ];
    }
}
