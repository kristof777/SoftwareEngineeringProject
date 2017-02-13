import { Injectable } from '@angular/core';
import {Http, ResponseContentType} from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class UserService {
    data: any;

    constructor(public http: Http) {
        this.data = null;
    }

    login(email: string, password: string, myFunc, navCont): void{

         //POST
        // this.http.post(URL, data, ResponseContentType.Json).subscribe(...)
        //GET
        // this.http.get(URL, ResponseContentType.Json).subscribe(...)

         this.http.post("http://localhost:8080/signin",
            { email: email, password: password }, ResponseContentType.Json)
             .subscribe(data => {
                this.data = data;
                 if(data["_body"] == "Hello")
                    myFunc(navCont);
             }, error => {
                 console.log("Oooops, sign in failed!");
             });

    }
    signUp(email:string,password:string, firstName:string,lastName:string, phoneNumber:string, city:string): void{


         this.http.post("http://localhost:8080/createuser",
            { email: email, password: password, firstName:firstName, lastName:lastName, phoneNumber:phoneNumber, city:city }, ResponseContentType.Json)
             .subscribe(data => {
                this.data = data;
                 console.log(this.data);

             }, error => {
                 console.log("Oooops, sign in failed!");
             });


    }


}
