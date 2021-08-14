import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";
import { tap } from "rxjs/operators";
import { User } from "./user.model";

interface AuthResponse {
    id: number;
    email: string;
    first_name: string,
    second_name: string,
    token: string;
}

@Injectable({
    providedIn: "root"
})
export class AuthService{

    user = new BehaviorSubject<User|null>(null);

    constructor(private http: HttpClient){ }

    signin(email: string, password: string){
        return this.http.post<AuthResponse>(
            "/api/user/login/",
            {
                username: email,
                password: password,
            }
        ).pipe(
            tap((resData: AuthResponse) => {
                this.handleAuthentication(resData)
            })
        )
    }

    signup(email: string, firstName: string, secondName: string, password: string){
        return this.http.post<AuthResponse>(
            "/api/user/create/",
            {
                username: email,
                first_name: firstName,
                second_name: secondName,
                password: password,
        }).pipe(
            tap((resData: AuthResponse) => {
                this.handleAuthentication(resData)
            })
        )
        
    }

    handleAuthentication(authResponse: AuthResponse) {
        const user = new User(
            authResponse.email, 
            authResponse.id, 
            authResponse.first_name,
            authResponse.second_name,
            authResponse.token
        );
        this.user.next(user)
        localStorage.setItem('userData', JSON.stringify(user));
    }

    autoLogin() {
        const userData = localStorage.getItem('userData');
        if (!userData){
            return
        }

        const parsedData = JSON.parse(userData)
        this.user.next(
            new User(
                parsedData.email,
                parsedData.id,
                parsedData.first_name,
                parsedData.second_name,
                parsedData._token,
            )
        )
    }
}