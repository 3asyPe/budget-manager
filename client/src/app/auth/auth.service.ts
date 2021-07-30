import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: "root"
})
export class AuthService{
    constructor(private http: HttpClient){ }

    signin(){
        return this.http.post<{test: string}>(
            "/api/test/",
            {
                test: "test"
            }
        )
    }
}